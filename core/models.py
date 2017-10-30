from django.db import models


class Newsletter(models.Model):
    email = models.EmailField(verbose_name='Email',max_length=255, null=False,
                              blank=False)
    created_at = models.DateTimeField(verbose_name='Criado em',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em',
                                      auto_now=True)

    class Meta:
        verbose_name = 'Inscrito'
        verbose_name_plural = 'Inscritos'
        ordering = ['-updated_at']
