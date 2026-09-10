from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignUpForm
from .mixins import SuperuserRequiredMixin, StaffPermissionRequiredMixin, StaffRequiredMixin


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class HomeView(TemplateView):
    template_name = 'home.html'


class StaffDashboardView(StaffRequiredMixin, TemplateView):
    template_name = 'accounts/staff_dashboard.html'


class UserDirectoryView(StaffPermissionRequiredMixin, TemplateView):
    permission_required = 'accounts.view_user'
    template_name = 'accounts/user_directory.html'


class StaffManagementView(SuperuserRequiredMixin, TemplateView):
    template_name = 'accounts/staff_management.html'
