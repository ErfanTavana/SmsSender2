from django.urls import path
from .views import DeviceLogCreateAPIView , ReceiveSMSAPIView

urlpatterns = [
    path('device_logs/', DeviceLogCreateAPIView.as_view(), name='device-log-create'),
    path('api/receive-sms/663489aa8de57a7c6534fbe0ad71b17be95fc82e/', ReceiveSMSAPIView.as_view(), name='receive-sms'),
]
