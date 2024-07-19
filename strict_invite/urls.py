from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name="index"),
    path('event_signup', views.user_profile_view, name='event_signup'),
    path('<str:pk>/', views.user_profile_detail, name='user_profile_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)