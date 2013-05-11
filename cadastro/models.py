from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from cadastro.utils import generic_get_absolute_url


"""
    dia_hora = models.DateTimeField()
    resumo = models.CharField(max_length=140)
    texto = models.TextField()
    tipo = models.SmallIntegerField(choices=TIPO_CLASSIFICACAO)
    turma = models.ForeignKey(Turma)
    email = models.EmailField(null=True, blank=True)
TIPO_CLASSIFICACAO = (
    (10, 'Cafe'),
    (20, 'Colacao'),
    (30, 'Almoco'),
    (40, 'Lanche'),
    (50, 'Janta')
    tipo = models.SmallIntegerField(choices=TIPO_CLASSIFICACAO)

"""

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
    endereco = models.TextField(null=True, blank=True)
    telefone = models.CharField(max_length=150, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    identidade = models.CharField(max_length=20, null=True, blank=True)
    orgao_expedidor = models.CharField(max_length=60, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class StatusCliente(models.Model):
    """
    Armazena os possiveis status dos Clientes
    """
    class Meta:
        verbose_name = 'Status Cliente'
        verbose_name_plural = 'Status Cliente'

    descricao = models.CharField(max_length=60)

    def __unicode__(self):
        return self.descricao

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

    data_cadastro = models.DateTimeField()
    status = models.ForeignKey(StatusCliente)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class StatusFuncionario(models.Model):
    """
    Armazena os possiveis status dos Funcionarios
    """
    class Meta:
        verbose_name = 'Status Funcionario'
        verbose_name_plural = 'Status Funcionario'

    descricao = models.CharField(max_length=60)
    habilitado = models.BooleanField()

    def __unicode__(self):
        return self.descricao

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Cargo(models.Model):
    """
    Armazena os possiveis Cargos do Salao
    """
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    descricao = models.CharField(max_length=60)

    def __unicode__(self):
        return self.descricao

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

    data_admissao = models.DateField()
    status = models.ForeignKey(StatusFuncionario)
    cargo = models.ForeignKey(Cargo)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class DependenteFuncionario(Pessoa):
    """
    Armazena os dependentes dos funcionarios
    """
    class Meta:
        verbose_name = 'Dependente Funcionario'
        verbose_name_plural = 'Dependentes Funcionario'
        ordering = ["nome"]

    funcionario = models.ForeignKey(Funcionario)

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class Especialidade(models.Model):
    """
    Armazena as possiveis especialidades.
    ex: manicure/pedicuri/corte/tintura/depilacao
    """
    class Meta:
        verbose_name = 'Especialidade'
        verbose_name_plural = 'Especialidades'

    descricao = models.CharField(max_length=60)

    def __unicode__(self):
        return self.descricao

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class EspecialidadeFuncionario(models.Model):
    """
    Armazena as possiveis especialidades de um Funcionario.
    """
    class Meta:
        verbose_name = 'Especialidade Funcionario'
        verbose_name_plural = 'Especialidades Funcionario'

    funcionario = models.ForeignKey(Funcionario)
    especialidade = models.ForeignKey(Especialidade)

    def __unicode__(self):
        return "%s %s" % ( self.funcionario.nome, self.especialidade.descricao )

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class Servico(models.Model):
    """
    Armazena os servicos realizados no salao
    """
    class Meta:
        verbose_name = 'Servico'
        verbose_name_plural = 'Servicos'

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=7,decimal_places=2)
    comissao = models.DecimalField(max_digits=5,decimal_places=2)
    custo_material = models.DecimalField(max_digits=7,decimal_places=2)
    especialidade = models.ForeignKey(Especialidade)
    habilitado = models.BooleanField()

    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PacoteServico(models.Model):
    """
    Armazena os pacotes de servicos exintes no salao
    """
    class Meta:
        verbose_name = 'Pacote Servico'
        verbose_name_plural = 'Pacotes de Servicos'

    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=7,decimal_places=2)
    habilitado = models.BooleanField()


    def __unicode__(self):
        return self.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class ServicoPacoteServico(models.Model):
    """
    Armazena os servicos contidos em cada pacote de servico
    """
    class Meta:
        verbose_name = 'Servico Contido em pacote'
        verbose_name_plural = 'Servicos Contidos em pacotes'

    pacote_servico = models.ForeignKey(PacoteServico, related_name = "pacote_servico_id")
    servico = models.ForeignKey(Servico)
    valor_rateado = models.DecimalField(max_digits=7,decimal_places=2)

    def __unicode__(self):
        return "%s" % self.servico.nome

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class HorarioDisponivel(models.Model):
    """
    Armazena os horarios disponiveis para marcacao
    """
    class Meta:
        verbose_name = 'Horario Disponivel'
        verbose_name_plural = 'Horarios Disponiveis'
        ordering = ["hora"]

    hora = models.TimeField()

    def __unicode__(self):
        return self.hora.strftime('%H:%M')

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class HorarioDisponivelFuncionario(models.Model):
    """
    Armazena os horarios disponiveis para marcacao
    """
    class Meta:
        verbose_name = 'Horario Disponivel Funcionario'
        verbose_name_plural = 'Horarios Disponiveis Funcionarios'
        ordering = ["data", "hora"]

    data = models.DateField()
    hora = models.ForeignKey(HorarioDisponivel)
    funcionario = models.ForeignKey(Funcionario)
    disponivel = models.BooleanField()

    def __unicode__(self):
        return "%s %s %s" % (self.data.strftime("%d/%m/%Y"), self.funcionario.nome, self.hora.hora.strftime('%H:%M'))

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class StatusPrestacaoServico(models.Model):
    """
    Armazena os possiveis status da PrestacaoServico.

    +-----------+-----------+---------------+-------------+
    | status    + realizado +   agendado    +  cancelado  |
    +-----------+-----------+---------------+-------------+
    | realizado +    true   +    false      +    false    |
    | cancelado +    false  +    false      +    true     |
    +-----------+-----------+---------------+-------------+
    Um item deve ser exibido para agendamento caso:
      - a) nao tenha agendamento, ou;
      - b) tenha um agendamento "realizado=false E Cancelado=true"
    """
    class Meta:
        verbose_name = 'Status Prestacao Servico'
        verbose_name_plural = 'Status Prestacao Servico'

    descricao_curta = models.CharField(max_length=20)
    descricao = models.CharField(max_length=60)
    realizado = models.BooleanField()
    cancelado = models.BooleanField()

    def __unicode__(self):
        return self.descricao

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PacoteServicoCliente(models.Model):
    """
    Armazena os pacotes de servico comprados pelo cliente
    """
    class Meta:
        verbose_name = 'Pacote Sevico Cliente'
        verbose_name_plural = 'Pacotes Sevico Clientes'

    cliente = models.ForeignKey(Cliente)
    recepcionista = models.ForeignKey(Funcionario)
    pacote_servico = models.ForeignKey(PacoteServico)
    pagamento = models.ForeignKey('Pagamento', null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.cliente.nome, self.pacote_servico.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PrestacaoServicoPacote(models.Model):
    """
    Armazena as prestaoes de servicos
    """
    class Meta:
        verbose_name = 'Prestacao Servico de Pacote'
        verbose_name_plural = 'Prestacoes de Servicos de Pacotes'

    status = models.ForeignKey(StatusPrestacaoServico)
    horario = models.ForeignKey(HorarioDisponivelFuncionario, null=True, blank=True)
    recepcionista = models.ForeignKey(Funcionario)
    servico_pacoteservico = models.ForeignKey(ServicoPacoteServico)
    pacoteServico_cliente = models.ForeignKey(PacoteServicoCliente)

    def __unicode__(self):
        return "%s %s" % (self.servico_pacoteservico.servico.nome, self.pacoteServico_cliente.cliente.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PrestacaoServico(models.Model):
    """
    Armazena as prestaoes de servicos
    """
    class Meta:
        verbose_name = 'Prestacao Servico'
        verbose_name_plural = 'Prestacoes de Servicos'

    status = models.ForeignKey(StatusPrestacaoServico)
    horario = models.ForeignKey(HorarioDisponivelFuncionario, null=True, blank=True)

    recepcionista = models.ForeignKey(Funcionario)
    cliente = models.ForeignKey(Cliente)
    servico = models.ForeignKey(Servico)
    pagamento = models.ForeignKey('Pagamento', null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.servico.nome, self.cliente.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)


class FormaPagamento(models.Model):
    """
    Armazena os possiveis formas de pagamento.
    """
    class Meta:
        verbose_name = 'Forma de Pagamento'
        verbose_name_plural = 'Formas de Pagamento'

    descricao = models.CharField(max_length=60)

    def __unicode__(self):
        return self.descricao

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class Pagamento(models.Model):
    """
    Armazena os pagamentos realizados
    """
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    recepcionista = models.ForeignKey(Funcionario)
    cliente = models.ForeignKey(Cliente)
    data_hora = models.DateTimeField()
    valor = models.DecimalField(max_digits=7,decimal_places=2)
    forma_pagamento = models.ForeignKey(FormaPagamento)

    def __unicode__(self):
        return "%s %s (%s)" % (self.cliente.nome, self.valor, self.forma_pagamento.descricao)

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
