from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, RegexValidator

from .models import Comment

class CommentForm(forms.ModelForm):
    comment = forms.CharField(validators=[MaxLengthValidator(10),
                                          RegexValidator(r'^[a-zA-Z0-9\s.]+$',
    'Only alphanumeric characters, spaces and full stops are allowed.')
                                          ])
    class Meta:
        model = Comment
        fields = ['comment']
    #comment = forms.CharField(required=True)