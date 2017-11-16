from django.conf.urls import url

from core import views


urlpatterns = [
        url(r'^$', views.landing_provider, name='core'),
        url(r'^home/$', views.home),
        url(r'^painel/$', views.dashboard_view, name='panel'),
        ]
