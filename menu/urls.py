from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('item/<int:item_id>/', views.menu_item_detail, name='menu_item_detail'),

    # MenuItem URLs
    path('menu-dashboard/', views.menu_dashboard, name='menu_dashboard'),
    path('dashboard/menu-items/', views.menu_item_list, name='menu_item_list'),
    path('dashboard/menu-items/create/', views.menu_item_create, name='menu_item_create'),
    path('dashboard/menu-items/update/<int:pk>/', views.menu_item_update, name='menu_item_update'),
    path('dashboard/menu-items/delete/<int:pk>/', views.menu_item_delete, name='menu_item_delete'),
    
    # MainCategory URLs
    path('dashboard/main-categories/', views.main_category_list, name='main_category_list'),
    path('dashboard/main-categories/create/', views.main_category_create, name='main_category_create'),
    path('dashboard/main-categories/update/<int:pk>/', views.main_category_update, name='main_category_update'),
    path('dashboard/main-categories/delete/<int:pk>/', views.main_category_delete, name='main_category_delete'),
    
    # Category URLs
    path('dashboard/categories/', views.category_list, name='category_list'),
    path('dashboard/categories/create/', views.category_create, name='category_create'),
    path('dashboard/categories/update/<int:pk>/', views.category_update, name='category_update'),
    path('dashboard/categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    # Tag URLs
    path('dashboard/tags/', views.tag_list, name='tag_list'),
    path('dashboard/tags/create/', views.tag_create, name='tag_create'),
    path('dashboard/tags/update/<int:pk>/', views.tag_update, name='tag_update'),
    path('dashboard/tags/delete/<int:pk>/', views.tag_delete, name='tag_delete'),

]