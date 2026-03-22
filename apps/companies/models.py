from django.db import models
from django.conf import settings
from roky_bot import settings

class Company(models.Model):
    name = models.CharField(max_length=255, name='name', unique=True)
    description = models.TextField(blank=True,name='description')
    balance = models.BigIntegerField(default=0,name='balance')

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        related_name='companies'
    )

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table='Companies'
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Membership(models.Model):
    class Roles(models.TextChoices):
        User = 'user', 'Пользователь'
        Admin = 'admin', 'Админ'
        SuperAdmin = 'superadmin', 'Супер Админ'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, related_name='memberships', null=False)
    company = models.ForeignKey(Company, models.CASCADE, related_name='memberships', null=False)
    role = models.TextField(default=Roles.User,max_length=20, choices=Roles.choices)
    is_active = models.BooleanField(max_length=20,default=True)

    def __str__(self):
        return f"{self.user.username}" + f"{self.role}"

    class Meta:
        db_table='Memberships'
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'
        unique_together= ('user','company')


class Video(models.Model):
    class Solution(models.IntegerChoices):
        Declined = 0, 'отклонено'
        Approved = 1, 'принято'
        Wait = 2, 'ожидает'

    member = models.ForeignKey(Membership, on_delete=models.CASCADE,related_name='uploded_videos',default=None, null=True)
    admin = models.ForeignKey(Membership, on_delete=models.SET_NULL, related_name='reviewed_videos',default=None,null=True, blank=True)
    link = models.CharField(max_length=255, unique=True, name='link')
    date = models.DateField(auto_now_add=True,name='date')
    solution = models.IntegerField(choices=Solution.choices, name = 'solution', default=Solution.Wait)
    
    class Meta:
        db_table='Videos'
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'