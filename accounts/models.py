# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin
from simple_email_confirmation.signals import email_confirmed

from accounts.helpers import (GENDER_CHOICES, STATUS_DOCUMENTS,
                              PROVIDER_CHOICES)



class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(SimpleEmailConfirmationUserMixin, AbstractBaseUser):
    objects = EmailUserManager()
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(
        _('active'), default=True, help_text=_(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_superuser = models.BooleanField(
        _('superuser status'), default=False, help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        )
    )
    is_staff = models.BooleanField(
        _('staff status'), default=False, help_text=_(
            'Designates whether the user can log into this admin '
            'site.'
        )
    )

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        return self.first_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    USERNAME_FIELD = 'email'


@receiver(email_confirmed)
def activate_user_handler(sender, **kwargs):
    sender.is_active = True
    sender.save()



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

