
from django import forms

from .models import Booking_models, Payment_status


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
        fields = ['seat','language','price','count']

class Payment_statusForm(forms.ModelForm):
    class Meta:
        model = Payment_status
        exclude = ['paydone']

    
