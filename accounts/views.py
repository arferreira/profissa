from django.urls import reverse
from django.views.generic import (FormView,
                                  TemplateView,
                                  UpdateView, RedirectView, CreateView)
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout as auth_logout, LoginView
from django.shortcuts import resolve_url
from django.core.urlresolvers import reverse_lazy


from .models import (User, Profile)
from .forms import (ProfileForm, UserAdminCreationForm)


# view responsável pelo registro dos usuários
class RegisterView(CreateView):
    model = User
    template_name = 'accounts/registration.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('accounts:update_profile')




class LoginView(LoginView):
    def get_success_url(self):
        return reverse(
                'accounts:update_profile')


# view responsável pela atualização do perfil de usuário
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template = 'accounts/profile_form.html'
    form_class = ProfileForm

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.request.user.pk)
        return user.profile

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdateProfileView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse(
                'accounts:update_profile')



# view responsável pelo logout de usuários
class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

logout = LogoutView.as_view()
