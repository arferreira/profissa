from django.db import models

# Model for Leads
class Lead(models.Model):
    first_name = models.CharField(max_length=200, blank=False, null=False,
                                  verbose_name='Primeiro Nome')
    last_name = models.CharField(max_length=200, blank=False, null=False,
                                 verbose_name='Sobrenome')
    cellphone = models.CharField(max_length=15, blank=False, null=False,
                                 verbose_name='Telefone/Celular')
    whatsapp = models.CharField(max_length=15, blank=False, null=False,
                                 verbose_name='Whatsapp')
    email = models.CharField(max_length=255, blank=True, null=False,
                             verbose_name='Email', unique=True)
    facebook = models.CharField(max_length=500, blank=True, null=False,
                                verbose_name='Página / Perfil Facebook')
    city_state = models.CharField(max_length=255, blank=False, null=False,
                                  verbose_name='Cidade / Estado')
    segment = models.CharField(max_length=255, blank=False, null=False,
                               verbose_name='Segmento de Negócio')
    suggestion = models.TextField(verbose_name='Sugestão')

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Criado em')
    SUBSCRIBE_CHOICES = (
            (True, 'Contactado por email'),
            (False, 'Não contactado'),
            )
    subscribe = models.BooleanField(verbose_name='Contactado',
                                    choices=SUBSCRIBE_CHOICES, default=False)

    class Meta:
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

