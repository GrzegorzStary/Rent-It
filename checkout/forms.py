from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Customize placeholders, CSS classes, remove labels,
        and autofocus on the first field.
        """
        super().__init__(*args, **kwargs)

        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2 (optional)',
            'town_or_city': 'Town or City',
            'postcode': 'Postcode',
            'county': 'County, State, or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True

        for field_name, field in self.fields.items():
            if field_name != 'country':
                placeholder = placeholders.get(field_name, '')
                if field.required:
                    placeholder += ' *'
                field.widget.attrs['placeholder'] = placeholder

            field.widget.attrs['class'] = 'stripe-style-input'
            field.label = False
