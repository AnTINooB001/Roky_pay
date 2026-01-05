"""
URL configuration for roky_bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from general import urls as gen_urls
from user_app import urls as users_urls
from companies import urls as comp_urls

urlpatterns = [
    path('admin/', admin.site.urls, name='superAdmin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include(users_urls, namespace='users')),
    path('companies/',include(comp_urls, namespace='company')),
    path('', include(gen_urls)),
]
