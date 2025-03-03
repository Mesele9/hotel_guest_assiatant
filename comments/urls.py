# comments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_view, name='feedback'),
    path('success/', views.feedback_success_view, name='feedback_success'),
    path('feedback-dashboard/', views.feedback_dashboard, name='feedback_dashboard'),
]
