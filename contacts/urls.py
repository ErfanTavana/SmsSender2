from django.urls import path
from .views import ContactApiView

urlpatterns = [
    path('create-contacts/', ContactApiView.as_view(), name='create-contacts'),  # ایجاد مخاطبین جدید
]
