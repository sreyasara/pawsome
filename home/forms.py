# form of order model
from django import forms
from .models import Address, Review


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'email', 'address_line_1', 'address_line_2', 'zip_code',
                  'district', 'phone_number']


class ReviewForm(forms.Form):
    class Meta:
        model = Review
        fields = ['review', 'rating']
