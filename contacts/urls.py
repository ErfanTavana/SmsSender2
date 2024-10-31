from django.urls import path
from .views import ContactApiView, ContactsView

urlpatterns = [
    path('create_contacts/', ContactApiView.as_view(), name='create-contacts'),  # ایجاد مخاطبین جدید
    path('contacts_list/', ContactsView.as_view(), name='contacts_list'),  # ایجاد مخاطبین جدید

]
