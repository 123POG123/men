from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView

from .forms import LoginUserForm, RegisterUserForm, UserPasswordChangeForm, ProfileUserForms


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'



class LogoutUserView(LogoutView):
    template_name = 'registration/logged_out.html'


class ProfileUserView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'



class ProfileEditUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForms
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_object(self):
        return self.request.user


class RegisterUserView(CreateView):
    template_name = "users/register.html"
    form_class = RegisterUserForm
    success_url = reverse_lazy('men:home')

    def form_valid(self, form):

        # form.groups.add(name='hello')
        form.save()
        return super().form_valid(form)


class UserPasswordChange(PasswordChangeView):
    template_name = "users/password_change_form.html"
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
