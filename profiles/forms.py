from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'bio',
            'profile_picture',
            'first_name',
            'last_name',
            'house_number',
            'street_name',
            'city',
            'postal_code'
        ]
widgets = {
    'bio': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Tell us something about yourself'}),
    'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
    'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
    'house_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House/Flat Number'}),
    'street_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Street Name'}),
    'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
    'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
}
