from django import forms
from django.contrib.auth.forms import UserCreationForm

from main.models import Pizza, OrderData


class RegistrationForm(UserCreationForm):
    """
    Расширенная форма регистрации пользователя.
    """
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
    """
    Форма добавления пиццы в ассортимент.
    """
    class Meta:
        model = Pizza
        fields = ('name', 'description', 'type', 'price', 'rating', 'image')
    name = forms.CharField(label='Название', max_length=255)
    description = forms.CharField(label='Описание', max_length=1000)
    type = forms.ChoiceField(label='Тип', choices=Pizza.TYPE_VARIANTS, initial=0, widget=forms.Select(attrs={'id' : 'pizza_type'}))
    price = forms.IntegerField(label='Цена', min_value=0)
    rating = forms.IntegerField(label='Рейтинг', min_value=0)
    image = forms.ImageField(label='Изображение')


class CheckoutForm(forms.ModelForm):
    """
    Форма добавления информации о пользователе (телефон и адрес) в базу данных.
    """
    class Meta:
        model = OrderData
        fields = ('phone', 'address')
    phone = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': '+7(xxx)xxx-xx-xx'
            }
        )
    )
    address = forms.CharField(
        label='Адрес доставки',
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Город Х, район У, улица Z, дом ХХХ, корпус ХХ, квартира Х'
            }
        )
    )
