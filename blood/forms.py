from django import forms
from .models import BloodDonationRequest
from account.models import Profile

class BloodDonationRequestForm(forms.ModelForm):
    class Meta:
        model = BloodDonationRequest
        fields = ['request_type', 'blood_type', 'region', 'province', 'municipality']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            profile = Profile.objects.get(user=user)
            if not profile.availability and self.instance.request_type == 'donating':
                self.fields['blood_type'].widget.attrs['readonly'] = True
                self.fields['region'].widget.attrs['readonly'] = True
                self.fields['province'].widget.attrs['readonly'] = True
                self.fields['municipality'].widget.attrs['readonly'] = True
                self.fields['blood_type'].initial = profile.blood_type
                self.fields['region'].initial = profile.region
                self.fields['province'].initial = profile.province
                self.fields['municipality'].initial = profile.municipality
