from django.db import models
from django.template.defaultfilters import slugify
from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import (Profile, User)


ADS_CHOICES = (
        (True, 'Ativado'),
        (False, 'Desativado'),
        )

BUDGET_PAID_CHOICES = (
        (True, 'Sim'),
        (False, 'Não'),
        )

BUDGET_FREE_CHOICES = (
        (True, 'Sim'),
        (False, 'Não'),
        )


# model referente a newsletter da app
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




# método referente a categorias de serviços dos profissionais
class Category(MPTTModel):
    description = models.CharField(max_length=100,
                                   verbose_name='Descrição')
    slug = models.SlugField(verbose_name='Atalho', max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='childrem', db_index=True)
    order = models.IntegerField(default=0, verbose_name='Sequência',
                                blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='Atualizado em')

    class MPTTMeta:
        order_insertion_by = ['description']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name = 'Segmento de Atuação'
        verbose_name_plural = 'Segmentos de Atuação'

    def __str__(self):
        ancestors = self.get_ancestors(ascending=False, include_self=True)
        return ' => '.join(category.description
                           for category in ancestors)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        super(Category, self).save(*args, **kwargs)




# model referente a configuração do perfil de profissional
class Configuration(models.Model):
    provider = models.OneToOneField(Profile, verbose_name='Profissional')
    skin = models.ImageField(upload_to='profiles_skin/',
                             verbose_name='Foto de capa', null=False,
                             blank=True)
    category = models.ForeignKey(Category, verbose_name='Segmento de Atuação')
    title = models.CharField(max_length=100, blank=True, null=True,
                             verbose_name='Título do seu negócio')
    url = models.SlugField(max_length=100, blank=False, null=False,
                           verbose_name='Url do seu negócio', unique=True)


    class Meta:
        verbose_name = 'Configuração'
        verbose_name_plural = 'Configurações'

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        self.url = slugify(self.url)
        super(Configuration, self).save(*args, **kwargs)


# modelo para profissionais
class Professional(models.Model):
    # Primeira carga de dados do anúncio
    user = models.OneToOneField(User, related_name='users_professional',
                                on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Segmento de atuação',
                                 blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False,
                             verbose_name='Título do anúncio', unique=True)
    slug = models.SlugField(verbose_name='Atalho para o anúncio',
                            blank=False, null=False, unique=True)
    description = models.TextField(verbose_name='Descrição do anúncio',
                                   blank=False, null=False)
    skills = models.CharField(max_length=255, verbose_name='Experiências',
                              blank=True, null=True)
    curriculum = models.TextField(verbose_name='Curriculum Vitae',
                                  blank=True, null=True)
    video = models.CharField(max_length=500, blank=True, null=True,
                             verbose_name='Seu vídeo de apresentação')
    # Carga de dados para endereço e orçamento
    main_address = models.CharField(max_length=500, blank=True, null=True,
                                    verbose_name='Seu endereço principal')
    budget_is_paid = models.BooleanField(blank=False, null=False,
                                         verbose_name='Orçamento é pago?',
                                         choices=BUDGET_PAID_CHOICES)
    # Carga de dados para cobranças
    base_price = models.DecimalField(max_digits=18, decimal_places=2,
                                     default=0,
                                     verbose_name='Preço base de seu trabalho')
    price_shit = models.DecimalField(max_digits=18, decimal_places=2,
                                     default=0,
                                     verbose_name='Valor de deslocamento'
                                     )
    price_detail = models.CharField(max_length=255, blank=True, null=True,
                                    verbose_name='Detalhe suas tarifas')
    budget_free = models.BooleanField(blank=False, null=False,
                                         verbose_name='Orçamento Grátis?',
                                         choices=BUDGET_PAID_CHOICES)
    picture = models.ImageField(upload_to='professional_picture/',
                               verbose_name='Foto', blank=False, null=False)
    skin = models.ImageField(upload_to='professional_skins/',
                               verbose_name='Skin', null=False, blank=True)

    created_at = models.DateTimeField(verbose_name='Criado em',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em',
                                      auto_now=True)

    STATUS_CHOICES = (
            (True, 'Publicado'),
            (False, 'Em análise'),
            )
    status = models.BooleanField(blank=False, null=False, default=False,
                                 verbose_name='Situação',
                                 choices=STATUS_CHOICES)

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Professional, self).save(*args, **kwargs)




# model referente aos anuncios de profissionais
class Ad(models.Model):
    user = models.ForeignKey(Profile, verbose_name='Usuário')
    category = models.ForeignKey(Category, verbose_name='Categoria',
                                 blank=False, null=False)
    title = models.CharField(max_length=255, blank=False, null=False,
                             verbose_name='Título do anúncio')
    slug = models.SlugField(verbose_name='Atalho para o anúncio',
                            max_length=255, unique=True)
    short_description = models.CharField(max_length=255, blank=True,
                                         null=False,
                                         verbose_name='Breve descrição')
    body = models.TextField(verbose_name='Descrição do anúncio')
    price = models.DecimalField(
            max_digits=18,
            decimal_places=2,
            default=0,
            verbose_name='Preço do anúncio'
            )
    status = models.BooleanField(verbose_name='Status do anúncio',
                                 default=False, null=False, blank=False,
                                 choices=ADS_CHOICES)
    created_at = models.DateTimeField(verbose_name='Criado em',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Atualizado em',
                                      auto_now=True)

    class Meta:
        verbose_name='Anúncio'
        verbose_name_plural='Anúncios'


    def __str__(self):
        return "%s - %s" % (self.title, self.provider)







