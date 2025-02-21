from django.shortcuts import render
#from django.contrib.auth.decorators import login_required
from .models import Hotel, Policy, Service, RoomType, LocalAttraction
from common_user.decorators import public_view


@public_view
def welcome(request):
    hotel = Hotel.objects.first()
    return render(request, 'directory/welcome.html', {'hotel': hotel})


@public_view
def policies(request):
    policies = Policy.objects.all()
    return render(request, 'directory/policies.html', {
        'general_policies': policies.filter(category='GEN'),
        'safety_policies': policies.filter(category='SAF'),
        'service_policies': policies.filter(category='SER'),
    })


@public_view
def services(request):
    services = Service.objects.all()
    return render(request, 'directory/services.html', {
        'services': services,
        '24h_services': services.filter(available_24h=True)
    })


@public_view
def attractions(request):
    return render(request, 'directory/attractions.html', {
        'attractions': LocalAttraction.objects.all()
    })


@public_view
def room_info(request):
    room_types = RoomType.objects.prefetch_related('amenities').all()
    return render(request, 'directory/room_info.html', {
        'room_types': room_types
    })