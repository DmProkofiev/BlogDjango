from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Расширенная модель пользавателя
    AbstractUser уже содержит username, first_name, last_name, email, password, is_staff...
    Мы добавляем свыои поля
    """
    phone = models.CharField('телефон',max_length=100, blank=True)
    city = models.CharField('город',max_length=100,blank=True,)
    avatar = models.ImageField('аватар', upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username