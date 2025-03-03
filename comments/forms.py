from django import forms
from .models import GuestFeedback, RatingCategory

class FeedbackForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email (optional)'}))
    exceptional_employee = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exceptional Employee (optional)'}))
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)
    dined_at_restaurant = forms.ChoiceField(
        choices=[('yes', 'Yes'), ('no', 'No')],
        widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Did you dine at our restaurant?'}),
        initial='no',
        label="Did you dine at our restaurant?"
    )

    class Meta:
        model = GuestFeedback
        fields = ['name', 'contact_no', 'email', 'date_of_stay', 'room_number', 'additional_comments', 'exceptional_employee']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'date_of_stay': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Date of Stay'}),
            'room_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Room Number'}),
            'additional_comments': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Additional Comments'}),
        }

    def clean_honeypot(self):
        if self.cleaned_data.get('honeypot'):
            raise forms.ValidationError("Spam detected")
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = RatingCategory.objects.all()
        for category in categories:
            required = category.name.lower() not in ['restaurant ambience', 'food quality']
            self.fields[f'rating_{category.id}'] = forms.IntegerField(
                label=category.name,
                widget=forms.HiddenInput(),
                min_value=1,
                max_value=5,
                required=required
            )