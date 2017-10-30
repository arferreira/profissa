# coding: utf-8
from django.conf.urls import url

from .views import (
    RegistrationView, RegistrationComplete,
    activation, ProfileView, UpdateProfileView)


urlpatterns = [
    url(r'^usuario/cadastre-se/$', RegistrationView.as_view(),
        name='registration'),
    url(r'^atualizar-perfil/$', UpdateProfileView.as_view(),
        name='update_profile'),
    url(r'^activation/', activation,
        name='activation'),
    url(r'^register/complete/$', RegistrationComplete.as_view(),
        name='registration_complete'),
    url(r'^perfil/$', ProfileView.as_view(),
        name='profile'),
]
