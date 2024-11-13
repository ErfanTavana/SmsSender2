# urls.py
from django.urls import path
from .views import LoginAPIView, LoginView, UserCreateView, UserListView, UserEditView, UserDeleteView, LogoutView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('login/', LoginView.as_view(), name='login'),

    path('user_create/', UserCreateView.as_view(), name='user_create'),

    path('user_list/', UserListView.as_view(), name='user_list'),

    path('user_edit/<uuid:user_id>/', UserEditView.as_view(), name='user_edit'),

    path('users/<uuid:user_id>/delete/', UserDeleteView.as_view(), name='user_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
