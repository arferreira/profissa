from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy


from .models import Lead



class InviteView(CreateView):
    model = Lead
    fields = ('first_name',
              'last_name',
              'cellphone',
              'whatsapp',
              'email',
              'facebook',
              'city_state',
              'segment',
              'suggestion')
    success_url = reverse_lazy('invite_success')

