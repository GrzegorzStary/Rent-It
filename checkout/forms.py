from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            "full_name", "email", "phone_number",
            "street_address1", "street_address2",
            "town_or_city", "postcode", "county", "country",
            "notes", "delivery_cost",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "full_name": "Full Name",
            "email": "Email Address",
            "phone_number": "Phone Number",
            "street_address1": "Street Address 1",
            "street_address2": "Street Address 2 (optional)",
            "town_or_city": "Town or City",
            "postcode": "Postcode",
            "county": "County, State, or Locality",
            "notes": "Notes (optional)",
            "delivery_cost": "0.00",
        }

        # Make optional fields not required
        self.fields["notes"].required = False
        self.fields["street_address2"].required = False
        self.fields["delivery_cost"].required = False

        # Autofocus on the first field
        if "full_name" in self.fields:
            self.fields["full_name"].widget.attrs["autofocus"] = True

        for name, field in self.fields.items():
            # Add placeholder text (optional, keeps form user-friendly)
            if name != "country":
                ph = placeholders.get(name, "")
                if field.required and name not in ("notes", "street_address2", "delivery_cost"):
                    ph += " *"
                field.widget.attrs["placeholder"] = ph

            # Apply Bootstrap / custom classes
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " stripe-style-input form-control").strip()

            # Classic labels: show them normally
            field.label = placeholders.get(name, name.replace("_", " ").title())
            field.label_suffix = ""  # removes colon
