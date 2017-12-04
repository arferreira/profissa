from django.shortcuts import (render, redirect)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http.response import (HttpResponseRedirect, Http404)
from django.core.urlresolvers import (reverse, reverse_lazy)

from accounts.models import Profile
from core.models import (Configuration, Ad, Professional)
from core.forms import (ProfileForm, ConfigurationForm, AdForm,
                        ProfessionalForm)

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


# view para o painel de controle do usuário
@login_required
def dashboard_view(request):
    try:
        complete_profile = request.user.profile.completed_profile()
        has_avatar = request.user.profile.has_avatar()
    except:
        raise Http404()
    context = {
            'complete_profile': complete_profile,
            'has_avatar': has_avatar
            }
    return render(request, 'dashboard.html', context)


# view para edição de profile do usuario
@login_required
def profile_edit(request):
    if Profile.objects.filter(user=request.user.pk).count():
        p = Profile.objects.filter(user=request.user.pk)[:1].get()
    else:
        p = Profile()
        p.user = request.user.pk
    if request.method == 'GET':
        form = ProfileForm(instance=p)
        context = {
                    'form': form,
                }
        return render(request,'profile.html', context)
    elif request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('root:profile_edit')
        return render(request, 'profile.html', {'form':form})



# view para editar configurações do perfil de usuário
@login_required
def configuration_professional_edit(request):
    if Configuration.objects.filter(provider=request.user.profile).count():
        c = Configuration.objects.filter(provider=request.user.profile)[:1]\
                                         .get()
    else:
        c = Configuration()
    c.provider = request.user.profile

    if request.method == 'GET':
        form = ConfigurationForm(instance=c)
        context = {
                    'form': form,
                }
        return render(request,'providers/configuration_professional.html',
                      context)
    elif request.method == 'POST':
        form = ConfigurationForm(request.POST, request.FILES, instance=c)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuração atualizada com sucesso!')
            return redirect('root:configuration_index')
        return render(request, 'providers/configuration_professional.html',
                      {'form':form})


@login_required
def solicitations(request):
    try:
        user = Profile.objects.get(user=request.user.pk)
        ads_count = Ad.objects.filter(user=user.pk).count()
        context = {
                'ads_count': ads_count
                }
    except:
        raise Http404()

    return render(request, 'solicitations.html', context)



@login_required
def ads(request):
    try:
        user = Profile.objects.get(user=request.user.pk)
        ads_count = Ad.objects.filter(user=user.pk).count()
        context = {
                'ads_count': ads_count
                }
    except:
        raise Http404()

    return render(request, 'clients/ads_index.html', context)


@login_required
def ad_new(request):
    if Professional.objects.filter(user=request.user.pk).count():
        p = Professional.objects.filter(user=request.user.pk)[:1].get()
    else:
        p = Professional()
        p.users_professional = request.user.pk
    if request.method == 'GET':
        form = ProfessionalForm(instance=p)
        context = {
                    'form': form,
                }
        return render(request,'ad_new.html', context)
    elif request.method == 'POST':
        form = ProfessionalForm(request.POST, request.FILES, instance=p)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anúncio criado com sucesso!')
            return redirect('root:ad_new')
        return render(request, 'ad_new.html', {'form':form})
