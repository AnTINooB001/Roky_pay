from django.db import models

class User_app_User(models.Model):
    balance = models.BigIntegerField(default=0,name='balance')
    system_admin = models.BooleanField(default=False,db_index=True)
    

    def __str__(self):
        return f"{self.username}"   
    
    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователи"

    
