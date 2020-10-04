from django import forms
from .models import JobApplication


class JobApplyForm(forms.ModelForm):
    # email = forms.EmailField()
    # resume = forms.FileField()

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'work_experience', 'resume']