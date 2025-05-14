from django.urls import path
from .views import DeviceLogCreateAPIView

urlpatterns = [
    path('device_logs/', DeviceLogCreateAPIView.as_view(), name='device-log-create'),
]
