from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, RegexValidator

from .models import Comment, Profile

class CommentForm(forms.ModelForm):
    comment = forms.CharField(validators=[MaxLengthValidator(10),
                                          RegexValidator(r'^[a-zA-Z0-9\s.]+$',
    'Only alphanumeric characters, spaces and full stops are allowed.')
                                          ])
    class Meta:
        model = Comment
        fields = ['comment']
    #comment = forms.CharField(required=True)

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

class ProfileForm(forms.ModelForm):
    credit_card = forms.CharField(max_length=20)
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth',
                  'save_payment_information']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EmailForm(forms.Form):
    email = forms.EmailField(required=True)

class EmailConfirmationForm(forms.Form):
    confirmation_code = forms.CharField(label='Confirmation Code', required=True, max_length=100)

class KYCForm(forms.Form):
    kyc_data = forms.CharField(label='KYC Data', max_length=100)
    file = forms.FileField(required=False)
    url = forms.URLField(label='URL', required=False)