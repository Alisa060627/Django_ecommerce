from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal'),

)
class CheckoutForm(forms.Form):
    street = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Landstrasse 1234'
    }))
    apartment = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suite'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget = CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',
        'id':'zip_code'}))

    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)
