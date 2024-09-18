# urls.py
from django.urls import path
from .views import admin_dashboard, edit_blood_request, delete_blood_request, edit_user, delete_user

urlpatterns = [
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin/edit_blood_request/<int:pk>/', edit_blood_request, name='edit_blood_request'),
    path('admin/delete_blood_request/<int:pk>/', delete_blood_request, name='delete_blood_request'),
    path('admin/edit_user/<int:pk>/', edit_user, name='edit_user'),
    path('admin/delete_user/<int:pk>/', delete_user, name='delete_user'),
    # other URL patterns
]
