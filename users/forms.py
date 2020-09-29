from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class UserRegisterForm(UserCreationForm):


    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    CHOICES =( 
        ("organization", "Organization"), 
        ("personal", "Personal"), 
    ) 
    # account_type = forms.CharField(max_length=200)
    account_type = forms.ChoiceField(choices = CHOICES)
    class Meta:
        model = Profile
        fields = ['account_type']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

