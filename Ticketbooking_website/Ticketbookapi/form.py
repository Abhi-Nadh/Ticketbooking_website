
from django import forms

from .models import Booking_models


class user_signup_form(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Username'}),required=True,max_length=50)
    email=forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder':'Email'}),required=True,max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=50)
    conf_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=50)
    
class user_login_form(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control','placeholder':'Username'}),required=True,max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=50)
# payment forms

class BookingModelForm(forms.ModelForm):
    class Meta:
        model = Booking_models
        fields = ['seat','price','count']

# class MovieSeatForm(forms.ModelForm):
#     seat = forms.ChoiceField()
#     price = forms.FloatField(disabled=True, initial=0)

#     class Meta:
#         model = Movie_seat
#         fields = ['seat','price','count']
    #     widgets = {
    #         'seat': forms.Select(attrs={'class': 'form-control', 'onchange': 'updatePrice()'}),
    #         'count': forms.NumberInput(attrs={'class': 'form-control'}),
    #     }
    #     labels = {
    #         'seat': 'Seat Type',
    #     }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     seat = cleaned_data.get('seat')

    #     if seat == 'diamond':
    #         cleaned_data['price'] = 300.0
    #     elif seat == 'gold':
    #         cleaned_data['price'] = 180.0
    #     elif seat == 'silver':
    #         cleaned_data['price'] = 120.0

    #     return cleaned_data
