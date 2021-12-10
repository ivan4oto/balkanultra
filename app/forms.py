from django import forms
from .models import UltraAthlete, SkyAthlete


class UltraAthleteForm(forms.ModelForm):
    class Meta:
        model = UltraAthlete
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'gender',
            'first_link',
            'second_link'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.EmailInput(attrs={'class': "form-control"}),
            'phone': forms.TextInput(attrs={'class': "form-control"}),
            'gender': forms.Select(attrs={'class': 'form-select'}, choices=[(1, 'male'), (2, 'female')]),
            'first_link': forms.TextInput(attrs={'class': "form-control"}),
            'second_link': forms.TextInput(attrs={'class': "form-control"}),
        }

class SkyAthleteForm(forms.ModelForm):
    class Meta:
        model = SkyAthlete
        fields = []
        widgets = {}