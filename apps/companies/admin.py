from django.contrib import admin
from .models import (
    Company,
    Membership,
    Video
)


@admin.register(Company)
class ComplaniesAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')


@admin.register(Membership)
class CompaniesMembersAdmin(admin.ModelAdmin):
    list_display = ('id','user__username','role', 'is_active','company')
    list_editable = ('role','is_active')
    
    
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'member__company', 'link', 'date', 'solution','admin')
    list_editable = ['solution',]