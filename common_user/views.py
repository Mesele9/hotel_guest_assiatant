
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


def generate_qr_code(url, color='black'):
    """Helper function to generate QR code"""
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

@public_view
def qr_code_page(request):
    # Generate URLs
    menu_url = request.build_absolute_uri('/menu')
    upload_url = request.build_absolute_uri('/upload')
    feedback_url = request.build_absolute_uri('/feedback')

    # Generate room numbers automatically
    room_qr_codes = {}
    floors = [1, 2, 3, 4, 5, 6]  # Floors from 1 to 6
    room_ranges = {1: range(101, 107),  # 101-106
                   2: range(201, 213),  # 201-212
                   3: range(301, 313),  # 301-312
                   4: range(401, 413),  # 401-412
                   5: range(501, 513),  # 501-512
                   6: range(601, 613)}  # 601-612

    for floor in floors:
        for room in room_ranges[floor]:
            room_url = request.build_absolute_uri(f'/room_directory/welcome/{room}/')
            room_qr_codes[str(room)] = generate_qr_code(room_url, color='#007FFF')

    context = {
        'menu_url': menu_url,
        'upload_url': upload_url,
        'feedback_url': feedback_url,
        'menu_qr': generate_qr_code(menu_url, color='#2c3e50'),
        'upload_qr': generate_qr_code(upload_url, color='#001F3F'),
        'feedback_qr': generate_qr_code(feedback_url, color='#001F3F'),
        'room_qr_codes': room_qr_codes,  # Dictionary of room_number: QR_code
    }
    return render(request, 'common_user/qr_code_page.html', context)
