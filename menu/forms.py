# forms.py
from django import forms
from .models import MainCategory, Category, Tag, MenuItem, Rating

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = MainCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CategoryForm(forms.ModelForm):
    main_category = forms.ModelChoiceField(
        queryset=MainCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = Category
        fields = ['name', 'main_category', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
                'style': 'width: 80px; height: 45px; padding: 0;'
            }),
        }

class MenuItemForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False
    )

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'image', 'is_active', 'categories', 'tags']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['guest_name', 'stars', 'comment']
        widgets = {
            'guest_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your name (optional)'
            }),
            'stars': forms.RadioSelect(attrs={'class': 'star-rating'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Share your experience... (optional)'
            }),
        }
        labels = {
            'stars': 'Your Rating'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stars'].widget.choices = [
            (i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)
        ]