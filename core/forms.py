from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import ModelForm, widgets
from django.utils.translation import ugettext as _
from django.forms.utils import ErrorList
import re


from core.models import (Configuration, Ad, Professional)
from accounts.models import (Profile)


class DateInput(forms.DateInput):
    input_type = 'date'


# Form para Profile
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
                'gender',
                'first_name',
                'last_name',
                'cpf',
                'birth_date',
                'phone_number',
                'whatsapp',
                ]


# Form para configurações do profissional
class ConfigurationForm(ModelForm):


    def __init__(self, *args, **kwargs):
        super(ConfigurationForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] =\
                "Um título legal para seu negócio"
        self.fields['url'].widget.attrs['placeholder'] =\
                "Um nome para link de seu Perfil"

    class Meta:
        model = Configuration
        fields = ['title', 'skin', 'category', 'url']


class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = ['title', 'short_description', 'category', 'body']



class ProfessionalForm(ModelForm):

    class Meta:
        model = Professional
        fields = [
                'category',
                'title',
                'description',
                'skills',
                'curriculum',
                'video',
                'main_address',
                'budget_is_paid',
                'base_price',
                'price_shit',
                'price_detail',
                'budget_free',
                'picture',
                'skin',
                ]
