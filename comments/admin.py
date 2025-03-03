from django.contrib import admin
from .models import RatingCategory, GuestFeedback, Rating

admin.site.register(RatingCategory)
admin.site.register(GuestFeedback)
admin.site.register(Rating)