# directory/views.py
from django.shortcuts import render, get_object_or_404
from .models import Hotel, Policy, Service, RoomType, LocalAttraction, Room
from common_user.decorators import public_view
from django.views.decorators.cache import cache_page


@public_view
@cache_page(60 * 60 * 1)  # Cache for 1 days
def welcome(request, room_number=None):
    hotel = Hotel.objects.first()  # Adjust for multi-hotel setups if needed
    room = None
    if room_number:
        try:
            room = get_object_or_404(Room, room_number=room_number, hotel=hotel)
        except:
            room = None  # Handle invalid room numbers gracefully
    return render(request, 'directory/welcome.html', {
        'hotel': hotel,
        'room': room,
        'room_number': room_number if room else None
    })


@public_view
@cache_page(60 * 60 * 3)  # Cache for 7 days
def services(request):
    room_number = request.GET.get('room_number')
    # Fetch all services once and filter in memory
    services = Service.objects.all()  # Single query
    return render(request, 'directory/services.html', {
        'services': services,
        '24h_services': [s for s in services if s.available_24h],  # In-memory filter
        'room_number': room_number
    })


@public_view
@cache_page(60 * 60 * 3)  # Cache for 7 days
def policies(request):
    room_number = request.GET.get('room_number')
    # Fetch all policies once and filter in memory
    policies = Policy.objects.all()  # Single query
    return render(request, 'directory/policies.html', {
        'general_policies': [p for p in policies if p.category == 'GEN'],
        'safety_policies': [p for p in policies if p.category == 'SAF'],
        'service_policies': [p for p in policies if p.category == 'SER'],
        'room_number': room_number
    })

@public_view
@cache_page(60 * 60 * 3)  # Cache for 7 days
def attractions(request):
    room_number = request.GET.get('room_number')
    return render(request, 'directory/attractions.html', {
        'attractions': LocalAttraction.objects.all(),
        'room_number': room_number
    })


@public_view
@cache_page(60 * 60 * 3)  # Cache for 7 days
def room_info(request):
    room_number = request.GET.get('room_number')
    room_types = RoomType.objects.prefetch_related('amenities').all()
    return render(request, 'directory/room_info.html', {
        'room_types': room_types,
        'room_number': room_number
    })