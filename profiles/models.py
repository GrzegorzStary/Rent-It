from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Import your existing utils module
from . import utils as profile_utils


def _geocode_via_utils(postcode):
    """
    Call function;
      geocode_postcode(lat, lng)
      geocode_uk_postcode {'postcode','lat','lng'}
    Returns (lat, lng, normalised_postcode_or_None)
    """
    if not postcode:
        return None, None, None

    fn = getattr(profile_utils, "geocode_postcode", None) or getattr(profile_utils, "geocode_uk_postcode", None)
    if not fn:
        return None, None, None

    try:
        res = fn(postcode)
    except Exception:
        return None, None, None

    # Handle tuple result
    if isinstance(res, tuple) and len(res) >= 2:
        lat, lng = res[0], res[1]
        return lat, lng, None

    # Handle dict result
    if isinstance(res, dict):
        lat = res.get("lat")
        lng = res.get("lng")
        normalised = res.get("postcode")
        return lat, lng, normalised

    return None, None, None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    house_number = models.CharField(max_length=50, blank=True, null=True)
    street_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # For geolocation auto filled from postcodes.io via utils
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, db_index=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(pre_save, sender=Profile)
def update_latlng_on_save(sender, instance: Profile, **kwargs):
    """
    Before saving a Profile, if the postal_code changed or lat/lng are empty,
    run geocoding via utils.
    """
    if not instance.postal_code:
        instance.lat = None
        instance.lng = None
        return

    postcode_changed = True
    if instance.pk:
        try:
            old = sender.objects.get(pk=instance.pk)
            old_pc = (old.postal_code or "").strip()
            new_pc = (instance.postal_code or "").strip()
            postcode_changed = (old_pc != new_pc)
        except sender.DoesNotExist:
            postcode_changed = True

    needs_geocode = postcode_changed or instance.lat is None or instance.lng is None
    if not needs_geocode:
        return

    lat, lng, normalised = _geocode_via_utils(instance.postal_code)

    if lat is not None and lng is not None:
        instance.lat = lat
        instance.lng = lng
        if normalised:
            instance.postal_code = normalised
    else:
        instance.lat = None
        instance.lng = None
