from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile



class UserRegisterForm(UserCreationForm):

#     GEEKS_CHOICES =( 
#     ("1", "Personal"), 
#     ("2", "Organization"), 
# ) 

    email = forms.EmailField()
    email2 = forms.EmailField()
    organization = forms.CharField()
    # account_type = forms.ChoiceField(choices = GEEKS_CHOICES) 

    class Meta:
        model = User
        fields = ['username','organization', 'email', 'email2', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']