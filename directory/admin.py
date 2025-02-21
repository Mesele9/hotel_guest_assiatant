from django.contrib import admin
from .models import *

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_number', 'updated_at')
    readonly_fields = ('updated_at',)

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)
    search_fields = ('title', 'content')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'available_24h', 'order')
    list_editable = ('order',)


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'max_occupancy')
    filter_horizontal = ('amenities',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'image')
        }),
        ('Pricing & Capacity', {
            'fields': ('base_price', 'max_occupancy', 'size_sqm')
        }),
        ('Amenities', {
            'fields': ('amenities',)
        }),
    )

@admin.register(LocalAttraction)
class LocalAttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'distance_from_hotel')
    search_fields = ('name', 'description')