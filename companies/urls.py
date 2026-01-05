from django.urls import path
from . import views

app_name='company'

urlpatterns = [
    path('<str:company_name>/home/', views.home, name='home')
]