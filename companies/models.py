from django.db import models
from django.conf import settings
from roky_bot import settings

class Companies(models.Model):
    name = models.CharField(max_length=255, name='name', unique=True)
    description = models.TextField(blank=True,name='description')
    balance = models.BigIntegerField(default=0,name='balance')

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Memberships',
        related_name='companies'
    )

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = 'Мои компании'
        verbose_name_plural = 'Мои компании'


class Memberships(models.Model):
    class Roles(models.TextChoices):
        User = 'user', 'Пользователь'
        Admin = 'admin', 'Админ'
        SuperAdmin = 'superadmin', 'Супер Админ'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='memberships', null=True)
    company = models.ForeignKey(Companies, models.CASCADE, related_name='memberships', null=True)
    role = models.TextField(default=Roles.User,max_length=20, choices=Roles.choices)
    is_active = models.BooleanField(max_length=20,default=True)

    def __str__(self):
        return f"{self.user.username}" + f"{self.role}"

    class Meta:
        verbose_name = 'Мои пользовтели'
        verbose_name_plural = 'Пользователи моих компаний'
        unique_together= ('user','company')


class Video(models.Model):
    class Solution(models.IntegerChoices):
        Declined = 0, 'отклонено'
        Approved = 1, 'принято'
        Wait = 2, 'ожидает'

    member = models.ForeignKey(Memberships, on_delete=models.CASCADE,related_name='uploded_videos',default=None, null=True)
    link = models.CharField(max_length=255, unique=True, name='link')
    date = models.DateField(auto_now_add=True,name='date')
    solution = models.IntegerField(choices=Solution.choices, name = 'solution', default=Solution.Wait)
    admin = models.ForeignKey(Memberships, on_delete=models.SET_NULL, related_name='reviewed_videos',default=None,null=True, blank=True)
    
    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'