from django import forms
from django.contrib.auth.forms import UserCreationForm

from main.models import Pizza


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


class PizzaCreationForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('name', 'description', 'type', 'price', 'rating', 'image')
    name = forms.CharField(label='Название', max_length=255)
    description = forms.CharField(label='Описание', max_length=1000)
    type = forms.ChoiceField(label='Тип', choices=Pizza.TYPE_VARIANTS, initial=0, widget=forms.Select(attrs={'id' : 'pizza_type'}))
    price = forms.IntegerField(label='Цена', min_value=0)
    rating = forms.IntegerField(label='Рейтинг', min_value=0)
    image = forms.ImageField(label='Изображение')
