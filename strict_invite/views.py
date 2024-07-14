import qrcode
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserProfileForm
from .models import User
from django.conf import settings
import os


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
            return redirect('user_profile_detail', user_profile.id)
    else:
        form = UserProfileForm()
    return render(request, 'user_profile_form.html', {'form': form})

def user_profile_detail(request, pk):
    user_profile = User.objects.get(pk=pk)
    qr_code_url = os.path.join(settings.MEDIA_URL, f'qrcodes/{pk}.png')
    return render(request, 'user_profile_detail.html', {'user_profile': user_profile, 'qr_code_url': qr_code_url})
