from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from social_django import urls as social_urls

from core import urls as core_urls
from accounts import urls as accounts_urls
from accounts.views import LoginView
from business.views import profile_public
from presentations.views import InviteView

urlpatterns = [
    # Administração Geral
    url(r'^management/', include(admin.site.urls)),

    # Captação de leads profissionais
    url(r'^profissional/', TemplateView.as_view(template_name='home.html'),
                            name='provider'),
    url(r'^pre-cadastro/sucesso/$',
        TemplateView.as_view(template_name='success.html'),
                             name='invite_success'),
    url(r'^pre-cadastro/$', InviteView.as_view(), name='invite'),

    # root do sistema
    url(r'', include(core_urls, namespace='root')),

    # Perfil público
    url(r'^perfil/$', profile_public),

    # Rotas de contas do usuário
    url(r'^conta/', include(accounts_urls, namespace='accounts')),
    url(r'^prestador/', include(core_urls, namespace='providers')),
    url(r'^contas/',include('allauth.urls')),
    url(r'^usuario/sair/$', logout,
        {'next_page': '/'}, name='logout'),
    url(
        r'^usuario/identifique-se/$',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login',
        kwargs={'template_name': 'accounts/login.html'}
        ),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
