import qrcode
import os

from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from helpers.utils import EmailService
from .forms import UserProfileForm
from .models import User


def user_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user_profile = form.save()
            url = request.build_absolute_uri(reverse('user_profile_detail', args=[user_profile.id]))
            qr = qrcode.make(url)
            qr_code_path = os.path.join(settings.MEDIA_ROOT, f'qrcodes/{user_profile.id}.png')
            os.makedirs(os.path.dirname(qr_code_path), exist_ok=True)
            qr.save(qr_code_path)

            EmailService.send_qr_code(
                user_profile.email, 
                qr_code_path,
                f'{user_profile.first_name} {user_profile.last_name}'
            )
            os.remove(qr_code_path)
            return redirect('user_profile_detail', user_profile.id)
    else:
        form = UserProfileForm()
    return render(request, 'user_event_form.html', {'form': form})

def user_profile_detail(request, pk):
    user_profile = User.objects.get(id=pk)
    qr_code_url = os.path.join(settings.MEDIA_URL, f'qrcodes/{pk}.png')
    return render(request, 'user_profile_detail.html', {'user_profile': user_profile, 'qr_code_url': qr_code_url})

def index(request):
    return render(request, 'index.html')
