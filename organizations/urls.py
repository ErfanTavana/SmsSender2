from django.urls import path
from .views import CreateGroup, GroupListView, EditGroupView, DeleteGroupView

urlpatterns = [
    path('create_group/', CreateGroup.as_view(), name='create_group'),
    path('group_list/', GroupListView.as_view(), name='group_list'),

    path('group/<int:group_id>/edit/', EditGroupView.as_view(), name='group_edit'),

    path('group/<int:group_id>/delete/', DeleteGroupView.as_view(), name='group_delete'),

]
