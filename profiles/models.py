from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, blank=False, default='Unknown')
    last_name = models.CharField(max_length=50, blank=False, default='Unknown')
    house_number = models.CharField(max_length=50, blank=False, default='Unknown')
    street_name = models.CharField(max_length=100, blank=False, default='Unknown')
    city = models.CharField(max_length=100, blank=False, default='Unknown')
    postal_code = models.CharField(max_length=20, blank=False, default='Unknown')
    phone_number = models.CharField(max_length=15, blank=False, default='Unknown')

    def __str__(self):
        return f'{self.user.username} Profile'


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='items/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
