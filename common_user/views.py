
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
    room_directory_url = request.build_absolute_uri('/room_directory')
    
    # Generate QR codes
    menu_qr = generate_qr_code(menu_url, color='#2c3e50')
    upload_qr = generate_qr_code(upload_url, color='#001F3F')
    feedback_qr = generate_qr_code(feedback_url, color='#001F3F')
    room_directory_qr = generate_qr_code(room_directory_url, color='#007FFF')

    context = {
        'menu_url': menu_url,
        'upload_url': upload_url,
        'feedback_url': feedback_url,
        'room_directory_url': room_directory_url,
        'menu_qr': menu_qr,
        'upload_qr': upload_qr,
        'feedback_qr': feedback_qr,
        'room_directory_qr': room_directory_qr
    }
    return render(request, 'common_user/qr_code_page.html', context)