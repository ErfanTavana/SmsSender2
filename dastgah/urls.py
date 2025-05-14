from django.urls import path
from .views import DeviceLogCreateAPIView

urlpatterns = [
    path('api/device-logs/', DeviceLogCreateAPIView.as_view(), name='device-log-create'),
]
