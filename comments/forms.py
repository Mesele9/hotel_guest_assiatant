from django import forms
from .models import GuestFeedback

RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = GuestFeedback
        fields = '__all__'
        widgets = {
            'date_of_stay': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'additional_comments': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'exceptional_employee': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        labels = {
            # Personal Information
            'name': 'Your Full Name',
            'contact_no': 'Contact Number',
            'email': 'Email Address',
            'date_of_stay': 'Date of Your Stay',
            
            # First Impression
            'welcome_rating': 'Your Welcome on Arrival',
            'reception_rating': 'Reception Experience',
            'hotel_cleanliness': 'Hotel Cleanliness & Tidiness',
            
            # Room Experience
            'room_cleanliness': 'Room Cleanliness',
            'amenities_rating': 'Room Amenities Quality',
            'room_service': 'Room Service Efficiency',
            'housekeeping': 'Housekeeping Service Quality',
            
            # Restaurant/Bar
            'restaurant_ambience': 'Restaurant/Bar Ambience',
            'waiting_team': 'Waiting Team Service',
            'complaint_response': 'Complaint Handling',
            'food_presentation': 'Food Presentation & Taste',
            'restaurant_setup': 'Restaurant Facilities',
            'toilet_cleanliness': 'Restroom Cleanliness',
            
            # Ordering Food
            'staff_recommendation': 'Staff Recommendations Quality',
            'waiting_time': 'Order Waiting Time',
            'food_temperature': 'Food Serving Temperature',
            'value_money': 'Value for Money',
            'portion_size': 'Portion Size Satisfaction',
            
            # Additional Fields
            'additional_comments': 'Your Additional Comments',
            'exceptional_employee': 'Exceptional Staff Member (if any)',
        }
        
        error_messages = {
            'name': {'required': "Please enter your full name"},
            'contact_no': {'required': "Please provide a contact number"},
            'email': {'required': "Please provide your email address"},
            'date_of_stay': {'required': "Please select your stay date"},
            'welcome_rating': {'required': "Please rate your welcome experience"},
            'reception_rating': {'required': "Please rate the reception experience"},
            'hotel_cleanliness': {'required': "Please rate hotel cleanliness"},
            'room_cleanliness': {'required': "Please rate room cleanliness"},
            'amenities_rating': {'required': "Please rate room amenities"},
            'room_service': {'required': "Please rate room service"},
            'housekeeping': {'required': "Please rate housekeeping service"},
            'restaurant_ambience': {'required': "Please rate restaurant ambience"},
            'waiting_team': {'required': "Please rate waiting team service"},
            'complaint_response': {'required': "Please rate complaint response"},
            'food_presentation': {'required': "Please rate food presentation"},
            'restaurant_setup': {'required': "Please rate restaurant setup"},
            'toilet_cleanliness': {'required': "Please rate restroom cleanliness"},
            'staff_recommendation': {'required': "Please rate staff recommendations"},
            'waiting_time': {'required': "Please rate order waiting time"},
            'food_temperature': {'required': "Please rate food temperature"},
            'value_money': {'required': "Please rate value for money"},
            'portion_size': {'required': "Please rate portion size"},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if isinstance(self.fields[field], forms.IntegerField):
                self.fields[field].widget = forms.RadioSelect(
                    choices=RATING_CHOICES,
                    attrs={'class': 'form-check-input'}
                )
                self.fields[field].error_messages = {
                    'required': f'Please provide rating for {self.fields[field].label.split(" Rating")[0].lower()}'
                }
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                if self.fields[field].required:
                    self.fields[field].widget.attrs['required'] = 'required'