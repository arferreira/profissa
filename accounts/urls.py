from django.conf.urls import url

from .views import (RegisterView, UpdateProfileView)


urlpatterns = [
    url(r'^cadastre-se/$', RegisterView.as_view(),
        name='register'),
    url(r'^atualizar-perfil/$', UpdateProfileView.as_view(),
        name='update_profile'),
]
