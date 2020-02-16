from django.urls import path
from .user_auth import UserRegisterView, UserLoginView, UserLogoutView
from .views import DevicesView, EntriesView


urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('devices', DevicesView.as_view(), name='devices'),
    path('devices/<str:device_id>/entries', EntriesView.as_view(), name='entries'),
]
