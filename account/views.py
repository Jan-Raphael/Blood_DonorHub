from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import UpdateView

from .models import Profile, BloodDonationRequest
from .forms import CustomUserCreationForm, ProfileForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')  # Redirect to login page after registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'account/register.html', {'form': form})

def home(request):
    return render(request, 'account/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                # Check if the user has a profile
                profile = Profile.objects.get(user=user)
                # If the profile exists, log in and redirect to the homepage
                auth_login(request, user)
                return redirect('home')
            except Profile.DoesNotExist:
                # If no profile, redirect to profile creation form
                return redirect('complete_profile')
        else:
            # Invalid login credentials
            return render(request, 'account/login.html', {'error': 'Invalid username or password'})
    return render(request, 'account/login.html')


@login_required
def complete_profile(request):
    if request.method == "POST":
        profile, created = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('view_profile')  # Redirect to view_profile after successful form submission
    else:
        profile = Profile.objects.filter(user=request.user).first()
        form = ProfileForm(instance=profile)

    return render(request, 'account/complete_profile.html', {'form': form})
@login_required
def view_profile(request):
    user_profile = get_object_or_404(Profile, user=request.user)
    donation_requests = BloodDonationRequest.objects.filter(user=request.user)
    context = {
        'profile': user_profile,
        'donation_requests': donation_requests,
    }
    return render(request, 'account/view_profile.html', context)

@login_required
def toggle_availability(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.availability = not profile.availability
    profile.save()
    return redirect('view_profile')

class ProfileUpdateView(UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'weight', 'height', 'region', 'province', 'municipality', 'availability']
    template_name = 'account/update_profile.html'
    success_url = reverse_lazy('view_profile')  # Redirect after successful update

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        profile = form.save(commit=False)

        # Check if availability is being changed
        if profile.availability and not self.object.availability:
            last_donation_date = self.object.last_donation_date
            if last_donation_date:
                days_since_last_donation = (timezone.now().date() - last_donation_date).days
                if days_since_last_donation < 56:
                    remaining_days = 56 - days_since_last_donation
                    form.add_error('availability', f'You must wait {remaining_days} more days before changing your availability.')
                    return self.form_invalid(form)

        profile.save()
        return super().form_valid(form)
