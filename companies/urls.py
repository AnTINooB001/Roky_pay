from django.urls import path
from . import views

app_name='company'

urlpatterns = [
    path('', views.CompanyView.as_view({'get': 'list', 'post': 'create'}), name='companies'),
    path('memberships/', views.MembershipView.as_view(), name='memberships'),
    path('memberships/manage/', views.MembershipUpdateView.as_view()),
    path('videos/admin/', views.VideoAdminView.as_view(), name='AdminVideo'),
    path('videos/user/',views.VideoUserView.as_view(), name='UserVideo')
]