# mini_fb/forms.py
# Form to collect inputs to create a new profile

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    '''Form for creating a new Profile'''

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image']

class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model=StatusMessage
        fields = ['message']