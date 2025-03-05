# common_user/views.py
import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import reverse
from django.utils.timezone import now
from django.http import HttpResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .decorators import role_required, public_view
from directory.models import Hotel, Room
from django.core.cache import cache
import qrcode
from io import BytesIO
import base64
from django.conf import settings


@public_view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            role_redirect = {
                'hr_staff': 'hr_dashboard',
                'store_staff': 'store_dashboard',
                'reception': 'upload_dashboard',
                'admin': 'admin_dashboard',
                'fb': 'menu_dashboard'
            }
            return redirect(role_redirect.get(user.role, 'login'))
            
        messages.error(request, 'Invalid credentials')
        return redirect('login')
        
    return render(request, 'common_user/login.html')


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@role_required('admin')
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('login')
    return render(request, 'common_user/admin_dashboard.html')


# Helper function to generate QR codes
def generate_qr_code(url, color='black'):
    """Generate a QR code from a URL with a specified fill color."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()


public_view
def qr_code_page(request):
    # Get the first hotel (adjust for multi-hotel setups if needed)
    hotel = Hotel.objects.first()
    if not hotel:
        # Gracefully handle the case where no hotel exists
        return render(request, 'common_user/qr_code_page.html', {'error': 'No hotel found.'})

    # Fetch rooms associated with the hotel
    rooms = Room.objects.filter(hotel=hotel)
    room_qr_codes = {}

    # Generate QR codes for each room
    for room in rooms:
        cache_key = f'qr_code_room_{room.room_number}'
        qr_code = cache.get(cache_key)
        if not qr_code:
            room_url = request.build_absolute_uri(reverse('welcome_room', args=[room.room_number]))
            qr_code = generate_qr_code(room_url, color='#001F3F')
            cache.set(cache_key, qr_code, timeout=2592000)  # Cache for 1 day
        room_qr_codes[room.room_number] = qr_code

    # Define static URLs upfront
    menu_url = request.build_absolute_uri('/menu')
    upload_url = request.build_absolute_uri('/upload')
    feedback_url = request.build_absolute_uri('/feedback')

    # Generate or retrieve cached QR codes for static URLs
    menu_qr = cache.get('menu_qr')
    if not menu_qr:
        menu_qr = generate_qr_code(menu_url, color='#2c3e50')
        cache.set('menu_qr', menu_qr, timeout=2592000)

    upload_qr = cache.get('upload_qr')
    if not upload_qr:
        upload_qr = generate_qr_code(upload_url, color='#001F3F')
        cache.set('upload_qr', upload_qr, timeout=2592000)

    feedback_qr = cache.get('feedback_qr')
    if not feedback_qr:
        feedback_qr = generate_qr_code(feedback_url, color='#001F3F')
        cache.set('feedback_qr', feedback_qr, timeout=2592000)

    # Build the context with all required variables
    context = {
        'menu_qr': menu_qr,
        'upload_qr': upload_qr,
        'feedback_qr': feedback_qr,
        'room_qr_codes': room_qr_codes,
        'menu_url': menu_url,
        'upload_url': upload_url,
        'feedback_url': feedback_url,
    }

    return render(request, 'common_user/qr_code_page.html', context)