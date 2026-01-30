from django.contrib import admin
from user_app.models import User



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'balance')
