from django.urls import path
from .views import ContactDashboardView

urlpatterns = [
    path('', ContactDashboardView.as_view(), name='home'),

]
