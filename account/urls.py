from django.urls import path
from . import views
from .views import view_profile, ProfileUpdateView, toggle_availability

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
path('login/', views.login_view, name='login'),
    path('complete-profile/', views.complete_profile, name='complete_profile'),
path('profile/', view_profile, name='view_profile'),

    path('profile/toggle_availability/', toggle_availability, name='toggle_availability'),

    path('profile/update/', ProfileUpdateView.as_view(), name='update_profile'),
]