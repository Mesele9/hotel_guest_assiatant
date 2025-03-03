from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import GuestFeedback, Rating, RatingCategory
from .forms import FeedbackForm
from django.db.models import Avg
from textblob import TextBlob

def public_view(view_func):
    return view_func

def role_required(role):
    def decorator(view_func):
        return login_required(view_func)
    return decorator

@public_view
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            dined = form.cleaned_data['dined_at_restaurant'] == 'yes'
            for category in RatingCategory.objects.all():
                field_name = f'rating_{category.id}'
                if field_name in form.cleaned_data and (dined or category.name.lower() not in ['restaurant ambience', 'food quality']):
                    score = form.cleaned_data[field_name]
                    if score:  # Only save if a score is provided
                        Rating.objects.create(feedback=feedback, category=category, score=score)
            send_mail(
                'New Feedback Submitted',
                f'Feedback from {feedback.name} received for room {feedback.room_number}.',
                'from@example.com',
                ['staff@example.com'],
                fail_silently=True,
            )
            if feedback.email:
                send_mail(
                    'Thank You for Your Feedback!',
                    'We appreciate your input. Enjoy 10% off your next stay with code THANKYOU10!',
                    'from@example.com',
                    [feedback.email],
                    fail_silently=True,
                )
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': '/feedback/success/'})
            return redirect('feedback_success')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors})
            return render(request, 'comments/feedback_form.html', {'form': form, 'categories': RatingCategory.objects.all()})
    else:
        form = FeedbackForm()
    return render(request, 'comments/feedback_form.html', {'form': form, 'categories': RatingCategory.objects.all()})

@public_view
def feedback_success_view(request):
    return render(request, 'comments/success.html')

@role_required('reception')
@login_required
def feedback_dashboard(request):
    feedbacks = GuestFeedback.objects.all()
    if 'date' in request.GET:
        feedbacks = feedbacks.filter(date_of_stay=request.GET['date'])
    if 'sort' in request.GET:
        feedbacks = feedbacks.order_by(request.GET['sort'])
    else:
        feedbacks = feedbacks.order_by('-created_at')
    for feedback in feedbacks:
        blob = TextBlob(feedback.additional_comments or '')
        feedback.sentiment = blob.sentiment.polarity
        feedback.overall_rating = feedback.ratings.aggregate(Avg('score'))['score__avg'] or 0
    context = {
        'feedbacks': feedbacks,
        'categories': RatingCategory.objects.all(),
    }
    return render(request, 'comments/feedback_dashboard.html', context)