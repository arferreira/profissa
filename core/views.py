from django.shortcuts import render
from django.views.generic import TemplateView


# view root do sistema
class LandingProviderView(TemplateView):
    template_name = 'root.html'

    def get_context_data(self, **kwargs):
        context = super(LandingProviderView, self).get_context_data(**kwargs)
        context['profissas'] = ['Antonio', 'Mariana', 'Rubiana', 'Alander']
        return context

landing_provider = LandingProviderView.as_view()


def home(request):
    return render(request, 'landing.html')


# view para o painel de usuário
def dashboard_view(request):
    if not request.user.profile.provider:
        template = 'clients/dashboard.html'
    else:
        template = 'providers/dashboard.html'
    return render(request, template)
