from django import forms
from .models import JobApplication
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.utils.translation import ugettext_lazy  as _


class JobApplyForm(forms.ModelForm):
    # email = forms.EmailField()
    # resume = forms.FileField()
    # phone = PhoneNumberField(
    #     label=_('phone number'),
    #     required=True,
    #     widget=PhoneNumberPrefixWidget(
    #         initial='NP',
    #         attrs={'placeholder': _('Phone number')}))

    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'work_experience', 'resume']