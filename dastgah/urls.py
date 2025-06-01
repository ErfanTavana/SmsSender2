from django.urls import path
from .views import DeviceLogCreateAPIView , ReceiveSMSAPIView

urlpatterns = [
    path('device_logs/', DeviceLogCreateAPIView.as_view(), name='device-log-create'),
    path('api/receive-sms/', ReceiveSMSAPIView.as_view(), name='receive-sms'),
]
