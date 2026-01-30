from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = 'users'

urlpatterns= [
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    path('profile/', views.user_profile, name='profile'),
    path('register/', views.user_register, name='register')
]