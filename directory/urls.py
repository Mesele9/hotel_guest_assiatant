# directory/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('services/', views.services, name='services'),
    path('policies/', views.policies, name='policies'),
    path('attractions/', views.attractions, name='attractions'),
    path('rooms/', views.room_info, name='room_info'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)