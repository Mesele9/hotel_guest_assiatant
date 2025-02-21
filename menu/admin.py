from django.contrib import admin
from django.utils.html import format_html  
from .models import MainCategory, Category, MenuItem, Rating, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color_preview')
    search_fields = ('name',)
    
    def color_preview(self, obj):
        return format_html(
            '<div style="background-color: {}; width: 24px; height: 24px; border-radius: 4px;"></div>',
            obj.color
        )
    color_preview.short_description = 'Color Preview'

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'main_category', 'description')
    list_filter = ('main_category',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags', 'categories')
    list_display = ('name', 'price', 'is_active')
    list_filter = ('is_active', 'categories')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'stars', 'guest_name', 'created_at')
    list_filter = ('stars',)
