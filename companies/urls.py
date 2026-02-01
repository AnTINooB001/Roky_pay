from django.urls import path
from . import views

app_name='company'

urlpatterns = [
    path('/', views.CompanyListApiView.as_view()),
    path('<str:company_name>/home/', views.home_view, name='home'),
    path('videos/patch/', views.set_video_solution_view, name='set_video_solution'),
    path('videos/get_video_to_admin_review/', views.get_video_to_admin_review_view),
    path('videos/post/' , views.create_video_by_user_view),
    path('post/', views.create_company_by_user_view),
]