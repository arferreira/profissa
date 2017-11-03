from django.urls import reverse
from django.views.generic import (FormView,
                                  TemplateView,
                                  UpdateView, RedirectView)
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import SuspiciousOperation
from django.contrib.auth import (
    get_backends,
    login as auth_login)
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout as auth_logout, LoginView
from django.shortcuts import resolve_url

from simple_email_confirmation.models import EmailAddress

from .models import (User, Profile)
from .forms import RegistrationForm, ProfileForm
from core.utils import EmailTemplate


class RegistrationView(FormView):
    template_name = 'accounts/registration.html'
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kargs):
        if not request.user.is_anonymous():
            return redirect(
                    'providers:dashboard')

        return super(RegistrationView, self).dispatch(request, args, kargs)

    def form_valid(self, form):
        user = form.save()
        activation_url = '%s://%s%s?activation_key=%s' % (
            self.request.scheme, self.request.get_host(),
            reverse('accounts:activation'),
            user.confirmation_key
        )
        mail = EmailTemplate(
            subject=u'Zummbee! - Account Activation', to=[user.email],
            from_email="Zummbee! <no-reply@zummbee.com.br>",
            tpl_message=u'accounts/email/activation.txt',
            tpl_alternative=u'accounts/email/activation.html',
            context={'activation_url': activation_url}
        )
        mail.send()
        return super(RegistrationView, self).form_valid(form)

    def get_success_url(self):
        return reverse('accounts:registration_complete')


def activation(request):
    activation_key = request.GET.get('activation_key', '')
    if not all((activation_key)):
        raise SuspiciousOperation
    try:
        address = EmailAddress.objects.confirm(
            activation_key)
        user = address.user
        backend = get_backends()[-1]  # Hack to bypass `authenticate()`.
        user.backend = "%s.%s" % (
            backend.__module__,
            backend.__class__.__name__)
        request.session.modified = True
        user.is_active = True
        user.save()
        auth_login(request, user)
    except (EmailAddress.DoesNotExist, EmailAddress.EmailConfirmationExpired):
        raise SuspiciousOperation

    url = "%s://%s:%s" % (request.scheme, settings.SESSION_COOKIE_DOMAIN,
                          settings.SESSION_COOKIE_PORT)

    return redirect(url)


class RegistrationComplete(TemplateView):
    template_name = 'accounts/registration_complete.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


class LoginView(LoginView):
    def get_success_url(self):
        return reverse(
                'accounts:update_profile')


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


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/usuario/identifique-se/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

logout = LogoutView.as_view()
