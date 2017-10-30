from django.conf.urls import url

from core.views import (dashboard, home, landing_provider)


urlpatterns = [
        url(r'^$', landing_provider, name='provider'),
        url(r'^home/$', home),
        url(r'^painel/$', dashboard, name='dashboard'),
        ]
