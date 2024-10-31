# urls.py
from django.urls import path
from .views import LoginAPIView, LoginView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('login/', LoginView.as_view(), name='login'),
]
