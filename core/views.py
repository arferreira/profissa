from django.shortcuts import render
from django.views.generic import TemplateView


class LandingProviderView(TemplateView):
    template_name = 'providers/landing_provider.html'

landing_provider = LandingProviderView.as_view()


def home(request):
    return render(request, 'landing.html')


def dashboard(request):
    return render(request, 'dashboard.html')
