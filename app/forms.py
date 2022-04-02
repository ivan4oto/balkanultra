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
            'first_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-first-name', 'placeholder': 'Име'}),
            'last_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-last-name','placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'id': 'post-mail', 'placeholder': 'Имеил'}),
            'phone': forms.TextInput(attrs={'class': "form-control", 'id': 'post-phone', 'placeholder': 'Телефон'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'post-gender'}, choices=[('male', 'male'), ('female', 'female')]),
            'first_link': forms.TextInput(attrs={'class': "form-control", 'id': 'post-first-link', 'placeholder': 'Линк 1'}),
            'second_link': forms.TextInput(attrs={'class': "form-control", 'id': 'post-second-link', 'placeholder': 'Линк 2'}),
        }

class SkyAthleteForm(forms.ModelForm):
    class Meta:
        model = SkyAthlete
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'gender'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-first-name', 'placeholder': 'Име'}),
            'last_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-last-name', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'id': 'post-mail','placeholder': 'Имеил'}),
            'phone': forms.TextInput(attrs={'class': "form-control", 'id': 'post-phone','placeholder': 'Телефон'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'post-gender'}, choices=[('male', 'male'), ('female', 'female')])
        }