from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'memberships', views.MembershipViewSet, basename='membership')

urlpatterns = [
    path('companies/', views.CompanyViewSet.as_view({'get': 'list', 'post': 'create'}), name='companies'),
    path('/', include(router.urls), name='memberships'),
    path('videos/admin/', views.VideoAdminView.as_view(), name='AdminVideo'),
    path('videos/user/',views.VideoUserView.as_view(), name='UserVideo')
]