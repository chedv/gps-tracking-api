from django.urls import path, re_path
from .views import (UserRegisterView, UserLoginView, UserLogoutView,
                    DeviceView, EntryView)


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('devices/', DeviceView.as_view(), name='devices'),
    re_path(r'^devices/(?P<device_id>[0-9a-f]{16})/entries/$', EntryView.as_view(), name='entries')
]
