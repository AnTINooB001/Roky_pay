from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, blank=False)
    first_name = models.CharField(max_length=255,blank=True)
    second_name = models.CharField(max_length=255, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['username']

    class Meta:
        verbose_name='Пользователь'
        verbose_name_plural='Пользователи'
    
    def __str__(self):
        return f"{self.email}"
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.second_name}'.strip()