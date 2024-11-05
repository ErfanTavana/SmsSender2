from django.urls import path
from .views import ContactCreateApiView, ContactCreateView, GroupListApiView, ContactListView, ContactDeleteView, \
    ContactEditView

urlpatterns = [
    path('api/group_list/', GroupListApiView.as_view(), name='api_group_list'),

    path('api/create_contacts/', ContactCreateApiView.as_view(), name='api_create_contacts'),
    path('contact_create/', ContactCreateView.as_view(), name='contact_create'),

    path('contact_list/', ContactListView.as_view(), name='contact_list'),
    path('contacts/edit/<int:contact_id>/', ContactEditView.as_view(), name='edit_contact'),
    path('contacts/delete/<int:contact_id>/', ContactDeleteView.as_view(), name='delete_contact'),

]
