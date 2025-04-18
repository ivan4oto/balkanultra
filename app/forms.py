from django import forms
from .models import UltraAthlete, SkyAthlete
from .services import is_string_numeric


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
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'post-gender'}, choices=[('male', 'Мъж'), ('female', 'Жена')]),
            'first_link': forms.TextInput(attrs={'class': "form-control", 'id': 'post-first-link', 'placeholder': 'Линк към състезание'}),
            'second_link': forms.TextInput(attrs={'class': "form-control", 'id': 'post-second-link', 'placeholder': 'Втори линк към състезание'}),
        }

class SkyAthleteForm(forms.ModelForm):
        
    captcha_answer = forms.CharField(
        label='Колко КМ дълга късата ни дистанция?',  # The question to be displayed
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Балкан Скай', 'id': 'post-captcha'})
    )

    class Meta:
        model = SkyAthlete
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'gender',
            'captcha_answer'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-first-name', 'placeholder': 'Име'}),
            'last_name': forms.TextInput(attrs={'class': "form-control", 'id': 'post-last-name', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'id': 'post-mail','placeholder': 'Имеил'}),
            'phone': forms.TextInput(attrs={'class': "form-control", 'id': 'post-phone','placeholder': 'Телефон'}),
            'gender': forms.Select(attrs={'class': 'form-select', 'id': 'post-gender'}, choices=[('male', 'Мъж'), ('female', 'Жена')])
        }


    def clean_captcha_answer(self):
        answer = self.cleaned_data.get('captcha_answer')
        if is_string_numeric(answer):
            answer = int(answer)
            # answer is 14 but if its in the 12-16 range we'll still let the user
            if answer//2 >= 6 and answer//2 <= 8:
                return answer
        raise forms.ValidationError('Incorrect answer. Please try again.')