from django.urls import path
from .views import MessagesCreateView, MessageListView, EditMessageView, DeleteMessageView

urlpatterns = [
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('messages_create/', MessagesCreateView.as_view(), name='messages_create'),

    path('message/edit/<int:message_id>/', EditMessageView.as_view(), name='message_edit'),

    path('messages/delete/<int:message_id>/', DeleteMessageView.as_view(), name='delete_message'),
]
