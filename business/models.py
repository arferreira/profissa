import uuid
from datetime import datetime

from django.db import models
from django.template.defaultfilters import slugify

from mptt.models import MPTTModel, TreeForeignKey

from accounts.models import Profile
from business.helpers import (SITUATION_RECEIPTS, BANKS)


# Manager for category model
class CategoryManager(models.Manager):
    def search(self, query):
        return self.get_queryset().filter(
            models.Q(description__icontains=query) | \
            models.Q(slug__icontains=query)
        )


# Model Category
class Category(MPTTModel):
    description = models.CharField(
        max_length=100,
        verbose_name='Descrição'
        )
    slug = models.SlugField(verbose_name='Atalho',
                            max_length=100)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
        )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class MPTTMeta:
        order_insertion_by = ['description']

    class Meta:
        unique_together = (('parent', 'slug',))
        verbose_name_plural = 'categories'


    # manager category with method search
    objects = CategoryManager()

    def get_name(self):
        return self.description

    def __str__(self):
        ancestors = self.get_ancestors(ascending=False, include_self=True)
        return ' => '.join(category.description
                           for category in ancestors)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.description)
        super(Category, self).save(*args, **kwargs)


class BankAccount(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False,
                                   verbose_name='Descrição da conta')
    bank = models.CharField(max_length=10, blank=False, null=False,
                            verbose_name='Banco', choices=BANKS)
    agency = models.CharField(max_length=20, blank=False, null=False,
                              verbose_name='Agência')
    number_account = models.CharField(max_length=20, blank=False, null=False,
                                      verbose_name='Número da conta')

    class Meta:
        verbose_name = 'Conta Bancária'
        verbose_name_plural = 'Contas Bancárias'

    def __str__(self):
        return self.description


# model to clients externs and interns
class Client(models.Model):
    profile = models.ForeignKey(Profile, blank=True, null=True)
    name = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Razão Social/Nome')
    phone_number = models.CharField(max_length=20, blank=True, null=False,
                                    verbose_name='Telefone')
    email = models.EmailField(blank=True, null=False, verbose_name='Email')
    """
        More info
    """
    alias = models.CharField(max_length=255, blank=True, null=False,
                             verbose_name='Apelido ou Nome de Fantasia')
    cpf_cnpj = models.CharField(max_length=255, blank=True, null=False,
                               verbose_name='CNPJ ou CPF')
    ie_rg = models.CharField(max_length=255, blank=True, null=False,
                             verbose_name='Inscrição Estadual ou RG')
    im = models.CharField(max_length=255, blank=True, null=False,
                          verbose_name='Inscrição Municipal')
    phone_secondary = models.CharField(max_length=20, blank=True, null=False,
                                       verbose_name='Telefone Secundário')
    site = models.CharField(max_length=500, blank=True, null=True,
                            verbose_name='Site')
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

    class Meta:
        verbose_name = 'Cliente/Fornecedor'
        verbose_name_plural = 'Clientes/Fornecedores'

    def __str__(self):
        if self.profile:
            return self.profile.user.first_name
        return self.name


# model to expenses
class Expenses(models.Model):
    profile = models.ForeignKey(Profile)
    client = models.ForeignKey(Client)
    number = models.CharField(max_length=20, blank=False, null=True,
                              verbose_name='Número', default=uuid.uuid4,
                              unique=True)
    description = models.CharField(max_length=255, blank=False, null=False,
                                   verbose_name='Descrição')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                                verbose_name='Valor financeiro')
    expiration_data = models.DateTimeField(verbose_name='Data de vencimento',
                                           null=False, blank=True)
    situation = models.IntegerField(blank=False, null=False, default=1,
                                    verbose_name='Situação',
                                    choices=SITUATION_RECEIPTS)
    attachment = models.ImageField(upload_to='attachment_receipts/',
                                   blank=True, verbose_name='Anexo')
    category = models.ForeignKey(Category, blank=True, null=True,
                                 verbose_name='Categoria')
    bank_account = models.ForeignKey(BankAccount, blank=True, null=True,
                                     verbose_name='Conta Bancária')

    class Meta:
        verbose_name = 'Despesa'
        verbose_name_plural = 'Despesas'

    def __str__(self):
        return self.description


# model to receipts
class Receipts(models.Model):
    profile = models.ForeignKey(Profile)
    client = models.ForeignKey(Client)
    number = models.CharField(max_length=20, blank=False, null=True,
                              verbose_name='Número', default=uuid.uuid4,
                              unique=True)
    description = models.CharField(max_length=255, blank=False, null=False,
                                   verbose_name='Descrição')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0,
                                verbose_name='Valor financeiro')
    expiration_data = models.DateTimeField(verbose_name='Data de vencimento',
                                           null=False, blank=True)
    situation = models.IntegerField(blank=False, null=False, default=1,
                                    verbose_name='Situação',
                                    choices=SITUATION_RECEIPTS)
    attachment = models.ImageField(upload_to='attachment_receipts/',
                                   blank=True, verbose_name='Anexo')
    category = models.ForeignKey(Category, blank=True, null=True,
                                 verbose_name='Categoria')
    bank_account = models.ForeignKey(BankAccount, blank=True, null=True,
                                     verbose_name='Conta Bancária')

    class Meta:
        verbose_name = 'Recebimento'
        verbose_name_plural = 'Recebimentos'

    def __str__(self):
        return self.description

class TypeService(models.Model):
    description = models.CharField(max_length=255, blank=False, null=False,
                                   verbose_name='Descrição')
    unit = models.CharField(max_length=20, blank=True, null=False,
                            verbose_name='Unidade de medida')
    unit_value = models.DecimalField(max_digits=8, decimal_places=2,
                                     blank=False, null=False,
                                     verbose_name='Valor unitário')
    municipal_code = models.CharField(max_length=100, blank=True, null=False,
                                      verbose_name='Código municipal')
    code_law_complement = models.CharField(max_length=255, blank=True,
                                           null=False,
                                           verbose_name='Código da lei' \
                                                        ' complementar')
    percent_tributes = models.IntegerField(blank=True, null=False, default=0,
                                           verbose_name='Percentual de' \
                                                        'tributos')
    iss_tributes = models.IntegerField(blank=True, null=False, default=0,
                                       verbose_name='Percentual do ISS')

    class Meta:
        verbose_name = 'Tipo de serviço'
        verbose_name_plural = 'Tipos de serviços'

    def __str__(self):
        return self.description


class OrderService(models.Model):
    number = models.CharField(max_length=20, blank=False, null=True,
                              verbose_name='Número', default=uuid.uuid4,
                              unique=True)
    person = models.ForeignKey(Client, blank=False, null=False,
                               verbose_name='Pessoa')
    emission_date = models.DateTimeField(blank=False, null=False,
                                         verbose_name='Data de emissão')
    obs = models.CharField(max_length=500, blank=True, null=False,
                           verbose_name='Observação')
    services = models.ManyToManyField(TypeService, blank=False, null=False,
                                      verbose_name='Itens')
    total = models.DecimalField(max_digits=8, decimal_places=2, blank=False,
                                null=False, verbose_name='Valor total')


    class Meta:
        verbose_name = 'Ordem de serviço'
        verbose_name_plural = 'Ordens de serviços'


    def __str__(self):
        return '{} - {}'.format(self.number, self.person.name)

