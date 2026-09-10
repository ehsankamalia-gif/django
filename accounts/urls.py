from django.urls import path

from . import api
from .views import SignUpView, StaffDashboardView, StaffManagementView, UserDirectoryView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('staff/', StaffDashboardView.as_view(), name='staff_dashboard'),
    path('staff/users/', UserDirectoryView.as_view(), name='user_directory'),
    path('staff/manage/', StaffManagementView.as_view(), name='staff_management'),
    path('api/users/', api.user_list, name='api_user_list'),
    path('api/users/<int:pk>/permissions/', api.user_permissions, name='api_user_permissions'),
    path('api/users/<int:pk>/role/', api.user_role, name='api_user_role'),
]
