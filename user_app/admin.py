from django.contrib import admin
from user_app.models import User


admin.site.register(User)

# @admin.register(Users)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username',)
#     #list_editable = []
