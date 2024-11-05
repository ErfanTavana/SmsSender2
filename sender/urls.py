from django.urls import path
from .views import CreateSmsProgramView, SmsProgramListView, SmsProgramDeleteView, SmsProgramEditView

urlpatterns = [
    path('create_sms_program/', CreateSmsProgramView.as_view(), name='create_sms_program'),
    path('sms_programs/', SmsProgramListView.as_view(), name='sms_program_list'),
    path('sms_program_edit/edit/<int:pk>/', SmsProgramEditView.as_view(), name='sms_program_edit'),

    path('sms_programs/delete/<int:pk>/', SmsProgramDeleteView.as_view(), name='sms_program_delete'),
]
