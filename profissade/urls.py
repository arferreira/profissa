from django.contrib import admin
from django.conf.urls import url, include
from django.contrib.auth.views import logout
from django.conf import settings
from django.conf.urls.static import static

from social_django import urls as social_urls

from core import urls as core_urls
from accounts import urls as accounts_urls
from accounts.views import LoginView
from business.views import profile_public

urlpatterns = [
    url(r'^$', include(core_urls, namespace='landing')),
    url(r'^perfil/$', profile_public),
    url(r'^conta/', include(accounts_urls, namespace='accounts')),
    url(r'^prestador/', include(core_urls, namespace='providers')),
    url(r'^admin/', admin.site.urls),
    url('', include(social_urls, namespace='social')),
    url(r'^usuario/sair/$', logout,
        {'next_page': '/usuario/identifique-se/'}, name='logout'),
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
