from django.urls import path
from .views import (
    BloodDonationRequestCreateView,
    BloodDonationRequestUpdateView,
    BloodDonationRequestDeleteView,
    BloodDonationRequestListView,
    BloodDonationRequestDetailView
)

urlpatterns = [
    path('create/', BloodDonationRequestCreateView.as_view(), name='blooddonationrequest_create'),
    path('update/<int:pk>/', BloodDonationRequestUpdateView.as_view(), name='blooddonationrequest_update'),
    path('delete/<int:pk>/', BloodDonationRequestDeleteView.as_view(), name='blooddonationrequest_delete'),
    path('list/', BloodDonationRequestListView.as_view(), name='blooddonationrequest_list'),
    path('detail/<int:pk>/', BloodDonationRequestDetailView.as_view(), name='blooddonationrequest_detail'),
]
