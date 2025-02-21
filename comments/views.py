# comments/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import GuestFeedback
from .forms import FeedbackForm
from django.db.models import Count
from common_user.decorators import public_view, role_required


@public_view
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('feedback_success')
        else:
            # Return form with errors
            return render(request, 'comments/feedback_form.html', {'form': form})
    else:
        form = FeedbackForm()
    return render(request, 'comments/feedback_form.html', {'form': form})


@public_view
def feedback_success_view(request):
    """Display success page after form submission"""
    return render(request, 'comments/success.html')


@role_required('reception')
@login_required
def feedback_dashboard(request):
    """Display comprehensive feedback dashboard"""
    feedbacks = GuestFeedback.objects.all().order_by('-submission_date')
    
    # Calculate average ratings for all categories
    avg_ratings = {
        'welcome': feedbacks.aggregate(Avg('welcome_rating'))['welcome_rating__avg'],
        'reception': feedbacks.aggregate(Avg('reception_rating'))['reception_rating__avg'],
        'hotel_cleanliness': feedbacks.aggregate(Avg('hotel_cleanliness'))['hotel_cleanliness__avg'],
        'room_cleanliness': feedbacks.aggregate(Avg('room_cleanliness'))['room_cleanliness__avg'],
        'amenities': feedbacks.aggregate(Avg('amenities_rating'))['amenities_rating__avg'],
        'room_service': feedbacks.aggregate(Avg('room_service'))['room_service__avg'],
        'housekeeping': feedbacks.aggregate(Avg('housekeeping'))['housekeeping__avg'],
        'restaurant_ambience': feedbacks.aggregate(Avg('restaurant_ambience'))['restaurant_ambience__avg'],
        'waiting_team': feedbacks.aggregate(Avg('waiting_team'))['waiting_team__avg'],
        'complaint_response': feedbacks.aggregate(Avg('complaint_response'))['complaint_response__avg'],
        'food_presentation': feedbacks.aggregate(Avg('food_presentation'))['food_presentation__avg'],
        'restaurant_setup': feedbacks.aggregate(Avg('restaurant_setup'))['restaurant_setup__avg'],
        'toilet_cleanliness': feedbacks.aggregate(Avg('toilet_cleanliness'))['toilet_cleanliness__avg'],
        'staff_recommendation': feedbacks.aggregate(Avg('staff_recommendation'))['staff_recommendation__avg'],
        'waiting_time': feedbacks.aggregate(Avg('waiting_time'))['waiting_time__avg'],
        'food_temperature': feedbacks.aggregate(Avg('food_temperature'))['food_temperature__avg'],
        'value_money': feedbacks.aggregate(Avg('value_money'))['value_money__avg'],
        'portion_size': feedbacks.aggregate(Avg('portion_size'))['portion_size__avg'],
    }

        # Calculate overall average manually
    overall_ratings = [fb.overall_rating for fb in feedbacks if fb.overall_rating is not None]
    avg_ratings['overall'] = sum(overall_ratings)/len(overall_ratings) if overall_ratings else 0


    # Add additional statistics
    context = {
        'feedbacks': feedbacks,
        'avg_ratings': avg_ratings,
        'total_feedbacks': feedbacks.count(),
        'feedback_with_comments': feedbacks.exclude(additional_comments__exact='').count(),
        'exceptional_employees': feedbacks.exclude(exceptional_employee__exact='')
                                          .values('exceptional_employee')
                                          .annotate(count=Count('exceptional_employee'))
                                          .order_by('-count')
    }
    
    return render(request, 'comments/feedback_dashboard.html', context)