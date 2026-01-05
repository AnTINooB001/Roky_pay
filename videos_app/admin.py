from django.contrib import admin
from videos_app.models import Video

# Register your models here.

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'link', 'date', 'solution','admin')
    list_editable = ['solution',]
