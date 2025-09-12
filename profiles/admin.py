from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "postal_code",
        "lat",
        "lng",
        "city",
        "phone_number",
    )
    search_fields = ("user__username", "postal_code", "city")
    list_filter = ("city",)

    # So Admin can edit user profiles from backend
    fields = (
        "user",
        "postal_code",
        "first_name",
        "last_name",
        "house_number",
        "street_name",
        "city",
        "phone_number",
        "lat",
        "lng",
        "bio",
        "profile_picture",
    )
    readonly_fields = ("lat", "lng")  # auto-set from postal_code
