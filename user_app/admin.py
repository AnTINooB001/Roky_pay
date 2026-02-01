from django.contrib import admin
from user_app.models import User_app_User



@admin.register(User_app_User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'balance')
