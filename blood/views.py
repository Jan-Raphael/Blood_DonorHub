from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import BloodDonationRequest
from .forms import BloodDonationRequestForm
from account.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin

class BloodDonationRequestCreateView(LoginRequiredMixin, CreateView):
    model = BloodDonationRequest
    form_class = BloodDonationRequestForm
    template_name = 'blood/blooddonationrequest_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if profile.availability == False and form.cleaned_data['request_type'] == 'donating':
            form.add_error(None, 'You cannot create a donating request because your availability is set to false.')
            return self.form_invalid(form)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_profile')

class BloodDonationRequestUpdateView(LoginRequiredMixin, UpdateView):
    model = BloodDonationRequest
    form_class = BloodDonationRequestForm
    template_name = 'blood/blooddonationrequest_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('view_profile')

    def get_queryset(self):
        return BloodDonationRequest.objects.filter(user=self.request.user, request_type='looking')

class BloodDonationRequestDeleteView(LoginRequiredMixin, DeleteView):
    model = BloodDonationRequest
    template_name = 'blood/blooddonationrequest_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('view_profile')

    def get_queryset(self):
        return BloodDonationRequest.objects.filter(user=self.request.user)

class BloodDonationRequestListView(LoginRequiredMixin, ListView):
    model = BloodDonationRequest
    template_name = 'blood/blooddonationrequest_list.html'

    def get_queryset(self):
        return BloodDonationRequest.objects.all()

class BloodDonationRequestDetailView(LoginRequiredMixin, DetailView):
    model = BloodDonationRequest
    template_name = 'blood/blooddonationrequest_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = get_object_or_404(Profile, user=self.object.user)
        return context

def some_view(request):
    from account.models import Profile