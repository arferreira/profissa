from django.conf.urls import url

from core import views


urlpatterns = [
        url(r'^$', views.landing_provider, name='core'),
        url(r'^home/$', views.home),
        url(r'^painel/$', views.dashboard_view, name='panel'),
        url(r'^meu-perfil/$',
                              views.profile_edit,
                              name='profile_edit'),
        url(r'^minhas-configuracoes/$',
                              views.configuration_professional_edit,
                              name='configuration_index'),
        url(r'^meus-solciitacoes-servicos/$',
                              views.solicitations,
                              name='solicitations_index'),
        url(r'^novo-anuncio/$',
                              views.ad_new,
                              name='ad_new'),
        ]
