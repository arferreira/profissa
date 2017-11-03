# coding: utf-8
from django import forms
from django.contrib.auth import get_user_model

from accounts.models import Profile

User = get_user_model()

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




class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    first_name = forms.CharField(label="Primeiro nome", required=True)
    last_name = forms.CharField(label="Último nome", required=True)
    password1 = forms.CharField(label='Password', required=True,
                                widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        required=True, widget=forms.PasswordInput
    )

    def clean_email(self):
        cleaned_email = self.cleaned_data.get('email')
        existing_users = User.objects.filter(email=cleaned_email)
        if existing_users:
                raise forms.ValidationError(
                    'Já existe um usuário com esse e-mail.'
                )
        return cleaned_email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            is_active=False,
        )
        user.set_password(data['password1'])
        user.save()
        return user
