from django.core.management.base import BaseCommand
from profiles.models import Profile


class Command(BaseCommand):
    help = "Re-geocode all profiles based on their postal codes."

    def handle(self, *args, **options):
        count = 0
        skipped = 0

        for profile in Profile.objects.all():
            if profile.postal_code:
                # Force re-geocode
                self.stdout.write(f"Re-geocoding {profile.user.username} at {profile.postal_code}...")
                profile.lat = None
                profile.lng = None
                profile.save()  # triggers pre_save signal to fetch coords
                count += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"Re-geocoded {count} profiles."))
        if skipped:
            self.stdout.write(self.style.WARNING(f"Skipped {skipped} profiles without postcodes."))
