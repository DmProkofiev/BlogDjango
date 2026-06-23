from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Форма регистрации
    наследование от UserCreationForm чтобы не писать проверку
    пароля вручную django сам проверит совпадение password1/password2
    и базовые правила пароля
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'city', 'avatar', 'password1', 'password2')

class CustomUserUpdateForm(forms.ModelForm):
    """
    форма редактирования профиля (кроме пароля)
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'city', 'avatar')