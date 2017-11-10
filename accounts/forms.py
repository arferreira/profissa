# coding: utf-8
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

User = get_user_model()

class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']


class DateInput(forms.DateInput):
    input_type = 'date'

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
                'avatar',
                'first_name',
                'last_name',
                'cpf',
                'rg',
                'birth_date',
                'gender',
                'bio',
                'phone_number',
                'whatsapp',
                'telegram',
                'zipcode',
                'country',
                'state',
                'city',
                'address',
                'address_number',
                'address_remark',
                'townhouse',
                'facebook',
                'provider'
                ]
        widgets = {
            'birth_date': DateInput()
        }


