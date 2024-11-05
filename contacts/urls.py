from django.urls import path
from .views import ContactCreateApiView, ContactsView, GroupListApiView

urlpatterns = [
    path('api/group_list/', GroupListApiView.as_view(), name='group_list'),

    path('api/create_contacts/', ContactCreateApiView.as_view(), name='create_contacts'),
    path('contacts_list/', ContactsView.as_view(), name='contacts_list'),

]
