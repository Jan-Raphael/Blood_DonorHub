# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import BloodDonationRequest
from .forms import BloodDonationRequestForm  # Ensure this form is created

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    blood_requests = BloodDonationRequest.objects.all()
    users = User.objects.all()
    return render(request, 'admin/dashboard.html', {'blood_requests': blood_requests, 'users': users})

@user_passes_test(is_admin)
def edit_blood_request(request, pk):
    blood_request = get_object_or_404(BloodDonationRequest, pk=pk)
    if request.method == 'POST':
        form = BloodDonationRequestForm(request.POST, instance=blood_request)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = BloodDonationRequestForm(instance=blood_request)
    return render(request, 'admin/edit_blood_request.html', {'form': form})

@user_passes_test(is_admin)
def delete_blood_request(request, pk):
    blood_request = get_object_or_404(BloodDonationRequest, pk=pk)
    if request.method == 'POST':
        blood_request.delete()
        return redirect('admin_dashboard')
    return render(request, 'admin/delete_blood_request.html', {'blood_request': blood_request})

@user_passes_test(is_admin)
def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if 'delete' in request.POST:
            user.delete()
            return redirect('admin_dashboard')
        # Add additional fields if necessary
    return render(request, 'admin/edit_user.html', {'user': user})

@user_passes_test(is_admin)
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')
    return render(request, 'admin/delete_user.html', {'user': user})
