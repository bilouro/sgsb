from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
from cadastro.utils import generic_get_absolute_url

class Pessoa(models.Model):
    """
    Classe com informacoes da pessoa
    Usada apenas indiretamente,  as classes Funcionario e Cliente especializam.
    """
    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ["nome"]

    nome = models.CharField(max_length=256)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Cliente(Pessoa):
    """
    Armazena informacoes dos Clientes
    """
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ["nome"]

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Funcionario(Pessoa):
    """
    Armazena informacoes dos Funcionarios
    """
    class Meta:
        verbose_name = 'Funcionario'
        verbose_name_plural = 'Funcionarios'
        ordering = ["nome"]

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class UserProfile(models.Model):
    """
    Permite buscar pelo usuario logado as classes de negocio ligadas a ele
    perfil_Funcionario = qual funcionario esta operando o sistema
    perfil_Cliente = permite simular um cliente acessando o site do cliente.
    """
    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'
        #ordering = ["nome"]

    user = models.OneToOneField(User)
    perfil_cliente = models.ForeignKey(Cliente, null=True, blank=True)
    perfil_funcionario = models.ForeignKey(Funcionario, null=True, blank=True)

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)
