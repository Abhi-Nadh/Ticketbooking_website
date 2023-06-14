from django import forms
from admin_show_site.models import Movie_details

# admin_login
class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                             'class': 'form-control', 'placeholder': 'Email'}), required=True, max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True, max_length=50)


class Add_Movie_Form(forms.ModelForm):
    class Meta:
        model = Movie_details
        # fields = ('__all__')
        exclude=('is_active',)
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
        # exclude=['duration']

# user login




