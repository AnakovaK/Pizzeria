from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Логин ',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Введите имя пользователя'
            }
        )
    )
    password1 = forms.CharField(
        label='Создайте пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Введите пароль'
            }
        )
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Повторите пароль'
            }
        )
    )


#class PizzaCreationForm(forms.ModelForm):
