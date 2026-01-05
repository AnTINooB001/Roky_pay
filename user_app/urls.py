from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'users'

urlpatterns= [
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    path('home/', views.user_home, name='home'),
    path('profile/', views.user_profile, name='profile'),
    path('send_video/', views.send_video, name='send_video'),
    path('register/', views.user_register, name='register')
]