from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import GuestFeedback, Rating, RatingCategory
from .forms import FeedbackForm
from django.db.models import Avg, Count, F, Value, FloatField
from django.db.models.functions import Coalesce
from textblob import TextBlob
import json
from common_user.decorators import public_view, role_required
from django.conf import settings 
from .tasks import send_feedback_email


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
                    if score:
                        Rating.objects.create(feedback=feedback, category=category, score=score)
            # Send staff email asynchronously
            send_feedback_email.delay(
                'New Feedback Submitted',
                f'Feedback from {feedback.name} received for room {feedback.room_number}.',
                ['staff@example.com']
            )
            if feedback.email:
                # Send success email asynchronously
                send_feedback_email.delay(
                    'Thank You for Your Feedback!',
                    'We appreciate your input.',
                    [feedback.email]
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
    
    # Apply filters
    date_filter = request.GET.get('date')
    if date_filter and date_filter.strip():
        feedbacks = feedbacks.filter(date_of_stay=date_filter)

    # Annotate overall_rating
    feedbacks = feedbacks.annotate(
        overall_rating=Coalesce(Avg('ratings__score'), Value(0.0), output_field=FloatField())
    )

    # Apply sorting
    sort_filter = request.GET.get('sort')
    if sort_filter:
        feedbacks = feedbacks.order_by(sort_filter)
    else:
        feedbacks = feedbacks.order_by('-created_at')

    # Calculate analytics
    total_feedbacks = feedbacks.count()
    feedback_with_comments = feedbacks.exclude(additional_comments='').count()
    avg_overall_rating = feedbacks.aggregate(Avg('overall_rating'))['overall_rating__avg'] or 0
    exceptional_employees = feedbacks.exclude(exceptional_employee='')\
        .values('exceptional_employee')\
        .annotate(count=Count('exceptional_employee'))\
        .order_by('-count')[:1]
    
    # Calculate category averages
    category_averages = RatingCategory.objects.annotate(
        avg_score=Avg('rating__score', filter=Rating.objects.filter(feedback__in=feedbacks).values('score'))
    ).values('name', 'avg_score')

    # Add sentiment and ratings to feedbacks
    for feedback in feedbacks:
        blob = TextBlob(feedback.additional_comments or '')
        feedback.sentiment = blob.sentiment.polarity
        feedback.verbose_ratings = {rating.category.name: rating.score for rating in feedback.ratings.all()}
        feedback.verbose_ratings_json = json.dumps(feedback.verbose_ratings)

    context = {
        'feedbacks': feedbacks,
        'categories': RatingCategory.objects.all(),
        'total_feedbacks': total_feedbacks,
        'feedback_with_comments': feedback_with_comments,
        'avg_overall_rating': avg_overall_rating,
        'exceptional_employees': exceptional_employees,
        'category_averages': list(category_averages),
    }
    return render(request, 'comments/feedback_dashboard.html', context)