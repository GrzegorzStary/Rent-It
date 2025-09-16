from django import forms
from .models import Profile
import requests


def geocode_uk_postcode(postcode: str):
    """Use postcodes.io to get lat/lng for a UK postcode."""
    cleaned = (
        postcode.strip().upper().replace("-", "").replace(".", "")
    )
    r = requests.get(
        f"https://api.postcodes.io/postcodes/{cleaned}",
        timeout=10,
    )
    data = r.json()
    if r.status_code == 200 and data.get("status") == 200:
        res = data["result"]
        return {
            "postcode": res[
                "postcode"
            ],  # normalized UK postcode format eg. N22 1AA
            "lat": res["latitude"],
            "lng": res["longitude"],
        }
    return None


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "profile_picture",
            "first_name",
            "last_name",
            "house_number",
            "street_name",
            "city",
            "postal_code",
        ]
        widgets = {
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 40,
                    "placeholder": "Tell us something about yourself",
                }
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First Name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last Name"}
            ),
            "house_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "House/Flat Number",
                }
            ),
            "street_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Street Name"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Postal Code"}
            ),
        }

    def clean_postal_code(self):
        code = self.cleaned_data["postal_code"]
        geo = geocode_uk_postcode(code)
        if not geo:
            raise forms.ValidationError(
                "Please enter a valid UK postcode."
            )
        self._geo = geo
        return geo["postcode"]

    def save(self, commit=True):
        obj = super().save(commit=False)
        if hasattr(self, "_geo"):
            obj.lat = self._geo["lat"]
            obj.lng = self._geo["lng"]
        if commit:
            obj.save()
        return obj
