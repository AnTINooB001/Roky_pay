from django.db import models
from companies import models as company_models
# Create your models here.

class Video(models.Model):
    class Solution(models.IntegerChoices):
        Declined = 0, 'Отклонено'
        Approved = 1, 'Принято'
        Wait = 2, 'Ожидает'

    member = models.ForeignKey(company_models.Memberships, on_delete=models.CASCADE,related_name='uploded_videos',default=None, null=True)
    link = models.CharField(max_length=255, name='link')
    date_created = models.DateField(auto_now_add=True,name='date')
    solution = models.IntegerField(choices=Solution.choices,
                                   name = 'solution',
                                   default=Solution.Wait)
    admin = models.ForeignKey(company_models.Memberships, on_delete=models.SET_NULL, related_name='reviewed_videos',default=None,null=True, blank=True)
    

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видео'