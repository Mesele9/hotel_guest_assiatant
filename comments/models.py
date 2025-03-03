from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class RatingCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class GuestFeedback(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(blank=True)  # Optional
    date_of_stay = models.DateField()
    room_number = models.CharField(max_length=10, blank=True)  # Track by room

    # Additional Fields
    additional_comments = models.TextField(blank=True)
    exceptional_employee = models.CharField(max_length=100, blank=True)  # Optional
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp
    updated_at = models.DateTimeField(auto_now=True)  # Update timestamp

    def __str__(self):
        return f"{self.name} - {self.date_of_stay}"

class Rating(models.Model):
    feedback = models.ForeignKey(GuestFeedback, related_name='ratings', on_delete=models.CASCADE)
    category = models.ForeignKey(RatingCategory, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.feedback} - {self.category}: {self.score}"