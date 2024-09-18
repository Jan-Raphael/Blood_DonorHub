from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class BloodDonationRequest(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('donating', 'Donating'),
        ('looking', 'Looking for'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPE_CHOICES)
    blood_type = models.CharField(max_length=10)
    region = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    municipality = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.request_type} request by {self.user}"