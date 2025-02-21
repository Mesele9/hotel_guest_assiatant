from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import json
from django.core.serializers.json import DjangoJSONEncoder


class GuestFeedback(models.Model):
    # Personal Information
    name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    date_of_stay = models.DateField()

    # First Impression
    welcome_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    reception_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    hotel_cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Room Experience
    room_cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    amenities_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    room_service = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    housekeeping = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Restaurant/Bar
    restaurant_ambience = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    waiting_team = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    complaint_response = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    food_presentation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    restaurant_setup = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    toilet_cleanliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Ordering Food
    staff_recommendation = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    waiting_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    food_temperature = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    value_money = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    portion_size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    # Additional Fields
    additional_comments = models.TextField(blank=True)
    exceptional_employee = models.CharField(max_length=100, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def get_all_ratings_json(self):
        return {
            'Welcome': self.welcome_rating,
            'Reception': self.reception_rating,
            'Hotel Cleanliness': self.hotel_cleanliness,
            'Room Cleanliness': self.room_cleanliness,
            'Amenities': self.amenities_rating,
            'Room Service': self.room_service,
            'Housekeeping': self.housekeeping,
            'Restaurant Ambience': self.restaurant_ambience,
            'Waiting Team': self.waiting_team,
            'Complaint Response': self.complaint_response,
            'Food Presentation': self.food_presentation,
            'Restaurant Setup': self.restaurant_setup,
            'Toilet Cleanliness': self.toilet_cleanliness,
            'Staff Recommendations': self.staff_recommendation,
            'Waiting Time': self.waiting_time,
            'Food Temperature': self.food_temperature,
            'Value for Money': self.value_money,
            'Portion Size': self.portion_size,
        }

    def get_verbose_ratings(self):
        """Return human-readable ratings with labels"""
        return [
            ('Your Welcome on Arrival', self.welcome_rating),
            ('Reception Experience', self.reception_rating),
            ('Hotel Cleanliness', self.hotel_cleanliness),
            ('Room Cleanliness', self.room_cleanliness),
            ('Room Amenities', self.amenities_rating),
            ('Room Service', self.room_service),
            ('Housekeeping', self.housekeeping),
            ('Restaurant Ambience', self.restaurant_ambience),
            ('Waiting Team', self.waiting_team),
            ('Complaint Response', self.complaint_response),
            ('Food Presentation', self.food_presentation),
            ('Restaurant Setup', self.restaurant_setup),
            ('Toilet Cleanliness', self.toilet_cleanliness),
            ('Staff Recommendations', self.staff_recommendation),
            ('Order Waiting Time', self.waiting_time),
            ('Food Temperature', self.food_temperature),
            ('Value for Money', self.value_money),
            ('Portion Size', self.portion_size),
        ]

    def get_verbose_ratings_json(self):
        return json.dumps(
            dict(self.get_verbose_ratings()),
            cls=DjangoJSONEncoder
        )

    '''@property
    def overall_rating(self):
        ratings = self.get_all_ratings_json().values()
        return round(sum(ratings) / len(ratings), 1)
    '''
    @property
    def overall_rating(self):
        ratings = [
            self.welcome_rating,
            self.reception_rating,
            self.hotel_cleanliness,
            self.room_cleanliness,
            self.amenities_rating,
            self.room_service,
            self.housekeeping,
            self.restaurant_ambience,
            self.waiting_team,
            self.complaint_response,
            self.food_presentation,
            self.restaurant_setup,
            self.toilet_cleanliness,
            self.staff_recommendation,
            self.waiting_time,
            self.food_temperature,
            self.value_money,
            self.portion_size,
        ]
        valid_ratings = [r for r in ratings if r is not None]
        return round(sum(valid_ratings)/len(valid_ratings), 1) if valid_ratings else 0

    def __str__(self):
        return f"{self.name} - {self.date_of_stay}"