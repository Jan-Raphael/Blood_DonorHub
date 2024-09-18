from django import forms
from .models import CustomUser, Profile

REGION_CHOICES = [
    ('Region III', 'Region III'),
    ('Region IV-A', 'Region IV-A'),
]

PROVINCE_CHOICES = {
    'Region III': [('Pampanga', 'Pampanga'), ('Tarlac', 'Tarlac')],
    'Region IV-A': [('Laguna', 'Laguna'), ('Cavite', 'Cavite')],
}

MUNICIPALITY_CHOICES = {
    'Pampanga': [('San Fernando', 'San Fernando'), ('Angeles', 'Angeles')],
    'Tarlac': [('Tarlac City', 'Tarlac City'), ('Concepcion', 'Concepcion')],
    'Laguna': [('Calamba', 'Calamba'), ('Santa Rosa', 'Santa Rosa')],
    'Cavite': [('Bacoor', 'Bacoor'), ('Dasmariñas', 'Dasmariñas')],
}

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'weight', 'height', 'region', 'province', 'municipality', 'blood_type', 'availability']
        widgets = {
            'region': forms.Select(choices=REGION_CHOICES),
            'province': forms.Select(choices=[]),
            'municipality': forms.Select(choices=[]),
        }

    def __init__(self, *args, **kwargs):
        region = kwargs.pop('region', None)
        province = kwargs.pop('province', None)
        super().__init__(*args, **kwargs)

        if region:
            self.fields['province'].choices = PROVINCE_CHOICES.get(region, [])
        if province:
            self.fields['municipality'].choices = MUNICIPALITY_CHOICES.get(province, [])