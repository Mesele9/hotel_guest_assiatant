from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=200)
    welcome_message = models.TextField()
    description = models.TextField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Policy(models.Model):
    CATEGORY_CHOICES = [
        ('GEN', 'General'),
        ('SAF', 'Safety'),
        ('SER', 'Services'),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Policies"
        ordering = ['order']

    def __str__(self):
        return self.title

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    available_24h = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

from django.db import models

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, 
                          help_text="Font Awesome icon class")
    
    def __str__(self):
        return self.name

class RoomType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_types/')
    amenities = models.ManyToManyField(Amenity, related_name='room_types')
    max_occupancy = models.PositiveIntegerField(default=2)
    size_sqm = models.PositiveIntegerField(help_text="Room size in square meters")

    def __str__(self):
        return self.name

    def get_amenities_list(self):
        return self.amenities.all().order_by('name')

        
class LocalAttraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    distance_from_hotel = models.CharField(max_length=50)
    image = models.ImageField(upload_to='attractions/')
    recommended_time = models.CharField(max_length=100)

    def __str__(self):
        return self.name