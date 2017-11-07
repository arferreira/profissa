import re

from django.db import models
from django.core import validators
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (AbstractBaseUser, UserManager,
                                        PermissionsMixin)


from accounts.helpers import (GENDER_CHOICES, STATUS_DOCUMENTS,
                              PROVIDER_CHOICES)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Apelido / Usuário', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .'
                , 'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de ' \
                     'forma única na plataforma'
    )
    email = models.EmailField(verbose_name='E-mail', unique=True)
    is_staff = models.BooleanField(verbose_name='Equipe', default=False)
    is_active = models.BooleanField(verbose_name='Ativo', default=True)
    date_joined = models.DateTimeField(auto_now_add=True,
                                       verbose_name='Data de entrada')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Atualizado em')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.email or self.username

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

# model to Profile User
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile',
                                on_delete=models.CASCADE)
    slug = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name='Apelido', unique=True)
    first_name = models.CharField(max_length=250, blank=True, null=False,
                                  verbose_name='Primeiro Nome')
    last_name = models.CharField(max_length=250, blank=True, null=False,
                                  verbose_name='Sobrenome')
    avatar = models.ImageField(upload_to='profile_avatar/',
                               verbose_name='Avatar')
    skin = models.ImageField(upload_to='profile_skin/',
                               verbose_name='Skin', null=False, blank=True)
    bio = models.TextField(max_length=500, verbose_name='Bio',
                           blank=True, null=False)
    location = models.CharField(max_length=30, verbose_name='Localização',
                                blank=True, null=False)
    birth_date = models.DateField(null=True, blank=True,
                                  verbose_name='Data de Nascimento')
    gender = models.CharField(blank=True, null=True, max_length=100,
                              choices=GENDER_CHOICES, verbose_name='Eu sou')
    """
        Personal Data

    """
    cpf = models.CharField(max_length=20, blank=True,
                           null=True, verbose_name='CPF')
    rg = models.CharField(max_length=20, blank=True,
                          null=True, verbose_name='RG')
    phone_number = models.CharField(max_length=20, blank=True,
                                    null=True, verbose_name='Telefone')
    whatsapp = models.CharField(max_length=20, blank=True,
                                null=True, verbose_name='Whatsapp')
    telegram = models.CharField(max_length=2, blank=True,
                                null=True, verbose_name='Telegram')
    facebook = models.CharField(max_length=500, blank=True, null=True,
                                verbose_name='Link do seu perfil ou página')
    """
        Location Data

    """
    zipcode = models.CharField(max_length=10, blank=True, null=True,
                               verbose_name='CEP')
    country = models.CharField(max_length=20, blank=True, null=True,
                               verbose_name='País', default='Brasil')
    state = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Estado')
    city = models.CharField(max_length=255, blank=True, null=True,
                            verbose_name='Cidade')
    address = models.CharField(max_length=500, blank=True, null=True,
                               verbose_name='Endereço')
    address_number = models.CharField(max_length=10, blank=True, null=True,
                                      verbose_name='Número')
    address_remark = models.CharField(max_length=500, blank=True, null=True,
                                      verbose_name='Complemento')
    townhouse = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name='Bairro')
    """
        Data Job

    """
    provider = models.BooleanField(default=False, blank=True, null=False,
                                   verbose_name='Prestador de serviço?',
                                   choices=PROVIDER_CHOICES)


    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

# model to documents profile
class Document(models.Model):
    profile = models.ForeignKey(Profile, blank=False, null=False,
                                on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='documents_profiles/', blank=False,
                                null=False, verbose_name='Foto do documento')
    selfie_document = models.ImageField(upload_to='selfies_documents/',
                                        blank=False, null=False,
                                        verbose_name='Selfie com o documento')
    status = models.BooleanField(default=False, choices=STATUS_DOCUMENTS,
                                 verbose_name='Status')

