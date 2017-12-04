# coding: utf-8
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de senha',
                                widget=forms.PasswordInput)


    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Email já cadastrado!")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                    "A confirmação de senha não está correta!"
                    )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.username = user.email
        if commit:
            user.save()
        return user


    class Meta:
        model = User
        fields = ('email', 'professional',)




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


