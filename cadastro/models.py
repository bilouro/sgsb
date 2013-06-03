import calendar
import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404
from django.utils import timezone
import itertools
from cadastro.utils import generic_get_absolute_url

ESTADOS = (
    ('RJ', 'Rio de Janeiro'),
    ('SP', 'Sao Paulo'),
)
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
    logradouro = models.CharField(max_length=150, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=60, null=True, blank=True)
    bairro = models.CharField(max_length=60, null=True, blank=True)
    cidade = models.CharField(max_length=80, null=True, blank=True)
    estado = models.CharField(max_length=2, null=True, blank=True, choices=ESTADOS)
    cep = models.CharField(max_length=9, null=True, blank=True)
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
    visto_em = models.DateTimeField()

    def atualiza_visto_em_agora(self):
        self.visto_em = timezone.datetime.now()
        self.save()

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

    def _especialidades(self):
        "Retorna as especialidades separado por virgula"
        especialidadefuncionario_list = EspecialidadeFuncionario.objects.filter(funcionario = self)
        return ', '.join([ef.especialidade.descricao for ef in especialidadefuncionario_list])

    especialidades = property(_especialidades)

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
        return "%s em %s as %sh" % (self.funcionario.nome, self.data.strftime("%d/%m/%Y"), self.hora.hora.strftime('%H:%M'))

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

    GERAR_SUCESSO=0
    GERAR_ERRO_HORARIO=1
    @staticmethod
    def gerar_mes(ano, funcionario_list, mes):
        if HorarioDisponivelFuncionario.objects.filter(data__year=ano).filter(data__month=mes).filter(funcionario__in=funcionario_list).count() > 0:
            return HorarioDisponivelFuncionario.GERAR_ERRO_HORARIO

        primeiro_dia_mes = datetime.date(ano, mes, 1)
        ult_dia_mes = calendar.monthrange(ano, mes)[1]
        de_zero_a_ult_dia_mes_list = range(ult_dia_mes)

        #busca os horarios disponiveis
        horario_disponivel_list = HorarioDisponivel.objects.all()
        for horario, funcionario, dias_a_somar in \
            itertools.product(
                    horario_disponivel_list,
                    funcionario_list,
                    de_zero_a_ult_dia_mes_list):

            hdf = HorarioDisponivelFuncionario()
            hdf.data = primeiro_dia_mes + \
                       datetime.timedelta(days=dias_a_somar)
            hdf.hora = horario
            hdf.funcionario = funcionario
            hdf.disponivel = True
            hdf.save()

        return HorarioDisponivelFuncionario.GERAR_SUCESSO




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
    NAO_AGENDADO='NAO_AGENDADO'
    REALIZADO='REALIZADO'
    CANCELADO='CANCELADO'
    AGENDADO='AGENDADO'

    cache={
        NAO_AGENDADO:None,
        REALIZADO:None,
        CANCELADO:None,
        AGENDADO:None,
        }

    class Meta:
        verbose_name = 'Status Prestacao Servico'
        verbose_name_plural = 'Status Prestacao Servico'

    descricao_curta = models.CharField(max_length=20)
    descricao = models.CharField(max_length=60)
    realizado = models.BooleanField()
    cancelado = models.BooleanField()

    def __unicode__(self):
        return self.descricao

    @staticmethod
    def getStatusPrestacaoServicoInstance(descricao_curta):
        if StatusPrestacaoServico.cache[descricao_curta] is None:
            StatusPrestacaoServico.cache[descricao_curta] = get_object_or_404(StatusPrestacaoServico, descricao_curta=descricao_curta)
        return StatusPrestacaoServico.cache[descricao_curta]

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

    def get_ultimo_servico_realizado(self):
        """
        retorna o ultimo(cronologicamente) servico com status_list realizado ou agendado, deste pacote, deste cliente.
        se nao achar, retorna None
        """
        prestacao_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente=self)
        prestacao_list = prestacao_list.filter(status__in=[StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.REALIZADO),
                                                           StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.AGENDADO)]) \
                                       .order_by('-horario__data', '-horario__hora__hora')

        return prestacao_list[0] if len(prestacao_list)>0 else None

    ultimo_servico_realizado = property(get_ultimo_servico_realizado)

    def get_status_servicos(self):
        """
        retorna um dicionario com a chave o STATUS e o valor count de servicos neste status
        Use pacote_servico_cliente.get_status_servicos()[StatusPrestacaoServico.REALIZADO]
        Use pacote_servico_cliente.get_status_servicos()['total'] para buscar o total de servicos
        """
        status = {}
        todas_psp_do_pacote_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente=self)
        status['total'] = todas_psp_do_pacote_list.count()
        for s in StatusPrestacaoServico.objects.all():
            status[s.descricao_curta] = todas_psp_do_pacote_list.filter(status__descricao_curta__in=[s.descricao_curta]).count()
        return status

    status_servicos = property(get_status_servicos)

    def _get_realizado(self):
        total = self.get_status_servicos()['total']
        realizado = self.get_status_servicos()[StatusPrestacaoServico.REALIZADO]
        if realizado == 0:
            return False
        else:
            if realizado == total:
                return True
            else:
                return None #significa que foi parcialmente

    realizado = property(_get_realizado)


    def __unicode__(self):
        return "%s - %s" % (self.cliente.nome, self.pacote_servico.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

DISCRIMINATOR = (
    ('SERVICO', 'Servico'),
    ('PACOTE', 'Pacote'),
)
class PrestacaoServico(models.Model):
    """
    Armazena as prestaoes de servicos
    """
    class Meta:
        verbose_name = 'Prestacao Servico'
        verbose_name_plural = 'Prestacoes de Servicos'
    SERVICO='SERVICO'
    PACOTE='PACOTE'

    status = models.ForeignKey(StatusPrestacaoServico)
    horario = models.ForeignKey(HorarioDisponivelFuncionario, null=True, blank=True)
    recepcionista = models.ForeignKey(Funcionario)
    discriminator = models.CharField(max_length=10, choices=DISCRIMINATOR)

    def __init__(self, *args, **kwargs):
        super(PrestacaoServico, self).__init__(*args, **kwargs)
        self.obj_filho = None

    CANCELAR_SUCESSO=0
    CANCELAR_ERRO_PRESTACAO=1
    CANCELAR_ERRO_TODAS_NAO_AGENDADAS=2
    CANCELAR_ERRO_JA_PAGO=3

    @staticmethod
    def cancelar(prestacao_servico):
        """
        cancela uma prestacao de servico/pacote de um cliente.
        o servico deve estar com status NAO_AGENDADO
        o pacote todos os servicos devem estar com status NAO_AGENDADO

        Muda o status de NAO_AGENDADO para CANCELADO
        RETURN_CODES:
            CANCELAR_SUCESSO=0
            CANCELAR_ERRO_PRESTACAO=1 -> Se o servico com status <> NAO_AGENDADO
            CANCELAR_ERRO_TODAS_NAO_AGENDADAS=2 -> Se um dos servicos do pacote com status <> NAO_AGENDADO
            CANCELAR_ERRO_JA_PAGO=3 Se o servico ou o pacote tiver pago nao podera cancelar.
        """
        cliente = prestacao_servico.cliente_object
        prestacao_servico_of_db= PrestacaoServico.objects.select_related('status').get(id=prestacao_servico.id)
        if prestacao_servico.discriminator == PrestacaoServico.SERVICO:
            if not prestacao_servico_of_db.status.descricao_curta == StatusPrestacaoServico.NAO_AGENDADO:
                return PrestacaoServico.CANCELAR_ERRO_PRESTACAO

            pss = get_object_or_404(PrestacaoServicoServico, id=prestacao_servico.id)
            if not pss.pagamento is None:
                return PrestacaoServico.CANCELAR_ERRO_JA_PAGO

        elif prestacao_servico.discriminator == PrestacaoServico.PACOTE:
            psp_clicada = get_object_or_404(PrestacaoServicoPacote, id=prestacao_servico.id)

            pacoteservico_cliente = psp_clicada.pacoteServico_cliente
            if not pacoteservico_cliente.pagamento is None:
                return PrestacaoServico.CANCELAR_ERRO_JA_PAGO

            todas_psp_do_pacote_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente=psp_clicada.pacoteServico_cliente)
            for psp in todas_psp_do_pacote_list:
                if not psp.status.descricao_curta == StatusPrestacaoServico.NAO_AGENDADO:
                    return PrestacaoServico.CANCELAR_ERRO_TODAS_NAO_AGENDADAS


        if prestacao_servico.discriminator == PrestacaoServico.SERVICO:
            #todo: depois que tiver feito um status cancelado para o pacote do cliente, passar a mudar o status para cancelado em vez de deletar
            prestacao_servico.delete()

        elif prestacao_servico.discriminator == PrestacaoServico.PACOTE:
            psp_clicada = get_object_or_404(PrestacaoServicoPacote, id=prestacao_servico.id)
            pacote_servico_cliente = psp_clicada.pacoteServico_cliente

            #CANCELAR O PACOTE DO CLIENTE
            #todo: fazer um status cancelado para o pacote do cliente
            todas_psp_do_pacote_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente=psp_clicada.pacoteServico_cliente)
            for psp in todas_psp_do_pacote_list:
                psp.delete()
            pacote_servico_cliente.delete()

        cliente.atualiza_visto_em_agora()
        return PrestacaoServico.CANCELAR_SUCESSO

    AGENDAR_SUCESSO=0
    AGENDAR_ERRO_HORARIO=1
    AGENDAR_ERRO_PRESTACAO=2
    @staticmethod
    def agendar(horario_funcionario, prestacao_servico):
        """
        Agenda um horario de um funcionario para uma prestacao de servico de um cliente.
        Muda o status de NAO_AGENDADO para AGENDADO
        Ocupa o horario do funcionario
        RETURN_CODES:
            AGENDAR_SUCESSO=0
            AGENDAR_ERRO_HORARIO=1 -> se o horario nao estiver disponivel
            AGENDAR_ERRO_PRESTACAO=2 -> se a prestacao nao estiver no status NAO_AGENDADA
        """
        if not get_object_or_404(HorarioDisponivelFuncionario, id=horario_funcionario.id).disponivel:
            return PrestacaoServico.AGENDAR_ERRO_HORARIO
        if not PrestacaoServico.objects.select_related('status').get(id=prestacao_servico.id).status.descricao_curta == StatusPrestacaoServico.NAO_AGENDADO:
            return PrestacaoServico.AGENDAR_ERRO_PRESTACAO

        #ajusta a prestacao
        status_novo = StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.AGENDADO)
        prestacao_servico.status = status_novo
        prestacao_servico.horario = horario_funcionario
        prestacao_servico.save()
        #ajusta horario_disponivel_funcionario
        horario_funcionario.disponivel = False
        horario_funcionario.save()

        prestacao_servico.cliente_object.atualiza_visto_em_agora()
        return PrestacaoServico.AGENDAR_SUCESSO

    DESAGENDAR_SUCESSO=0
    DESAGENDAR_ERRO_HORARIO=1
    DESAGENDAR_ERRO_PRESTACAO=2
    @staticmethod
    def desagenda(prestacao_servico):
        """
        DESAgenda um horario de um funcionario para uma prestacao de servico de um cliente.
        Muda o status de AGENDADO para NAO_AGENDADO
        Torna disponivel o horario do funcionario
        RETURN_CODES:
            DESAGENDAR_SUCESSO=0
            DESAGENDAR_ERRO_HORARIO=1 -> se o horario nao estiver ocupado
            DESAGENDAR_ERRO_PRESTACAO=2 -> se a prestacao nao estiver no status AGENDADA ou se nao tiver horario associado
        """
        horario_funcionario = prestacao_servico.horario
        prestacao_servico_of_db= PrestacaoServico.objects.select_related('status').get(id=prestacao_servico.id)
        if not prestacao_servico_of_db.status.descricao_curta == StatusPrestacaoServico.AGENDADO or \
                        prestacao_servico_of_db.horario is None:
            return PrestacaoServico.DESAGENDAR_ERRO_PRESTACAO
        if get_object_or_404(HorarioDisponivelFuncionario, id=horario_funcionario.id).disponivel:
            return PrestacaoServico.DESAGENDAR_ERRO_HORARIO

        horario_funcionario.disponivel = True
        horario_funcionario.save()

        prestacao_servico.horario = None
        prestacao_servico.status = StatusPrestacaoServico.getStatusPrestacaoServicoInstance(
            StatusPrestacaoServico.NAO_AGENDADO)
        prestacao_servico.save()

        prestacao_servico.cliente_object.atualiza_visto_em_agora()
        return PrestacaoServico.DESAGENDAR_SUCESSO

    REALIZAR_SUCESSO=0
    REALIZAR_ERRO_PRESTACAO=1
    @staticmethod
    def realizar(prestacao_servico):
        """
        realiza uma prestacao de servico de um cliente.
        Muda o status de AGENDADO para REALIZADO
        RETURN_CODES:
            REALIZAR_SUCESSO=0
            REALIZAR_ERRO_PRESTACAO=2 -> se a prestacao nao estiver no status AGENDADA
        """
        prestacao_servico_of_db= PrestacaoServico.objects.select_related('status').get(id=prestacao_servico.id)
        if not prestacao_servico_of_db.status.descricao_curta == StatusPrestacaoServico.AGENDADO:
            return PrestacaoServico.REALIZAR_ERRO_PRESTACAO

        prestacao_servico.status = StatusPrestacaoServico.getStatusPrestacaoServicoInstance(
            StatusPrestacaoServico.REALIZADO)
        prestacao_servico.save()

        prestacao_servico.cliente_object.atualiza_visto_em_agora()
        return PrestacaoServico.REALIZAR_SUCESSO

    DESREALIZAR_SUCESSO=0
    DESREALIZAR_ERRO_PRESTACAO=1
    @staticmethod
    def desrealizar(prestacao_servico):
        """
        desrealiza uma prestacao de servico de um cliente.
        Muda o status de REALIZADO para AGENDADO
        RETURN_CODES:
            DESREALIZAR_SUCESSO=0
            DESREALIZAR_ERRO_PRESTACAO=1 -> se a prestacao nao estiver no status REALIZADO
        """
        prestacao_servico_of_db= PrestacaoServico.objects.select_related('status').get(id=prestacao_servico.id)
        if not prestacao_servico_of_db.status.descricao_curta == StatusPrestacaoServico.REALIZADO:
            return PrestacaoServico.DESREALIZAR_ERRO_PRESTACAO

        prestacao_servico.status = StatusPrestacaoServico.getStatusPrestacaoServicoInstance(
            StatusPrestacaoServico.AGENDADO)
        prestacao_servico.save()

        prestacao_servico.cliente_object.atualiza_visto_em_agora()
        return PrestacaoServico.DESREALIZAR_SUCESSO

    @staticmethod
    def novo_servico(cliente, servico, recepcionista):
        """
        Cria um servico uma prestacao de servico (avulsa) para um cliente.
        Com o status NAO_AGENDADO
        RETURN_CODES:
            SUCESSO=Retorna o objeto
            Erro=eh levantada uma excecao que interrompe o processo.
        """
        prestacao_servico = PrestacaoServicoServico.objects.create(cliente=cliente,
                                               servico=servico,
                                               status=StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.NAO_AGENDADO),
                                               discriminator=PrestacaoServico.SERVICO,
                                               recepcionista=recepcionista,
                                               )

        prestacao_servico.cliente_object.atualiza_visto_em_agora()
        return prestacao_servico

    @staticmethod
    def novo_pacote(cliente, pacote, recepcionista):
        """
        Cria um pacote de servicos e adiciona todos os servicos para o cliente
        Com o status NAO_AGENDADO
        RETURN_CODES:
            SUCESSO=Retorna o pacote
            Erro=eh levantada uma excecao que interrompe o processo.
        """
        #1 adiciona o pacote do cliente
        pacote_cliente = PacoteServicoCliente.objects.create(cliente=cliente,
                                            recepcionista=recepcionista,
                                            pacote_servico=pacote,
                                            )

        #2 adiciona cada servico do pacote comprado
        #  busca todos os servicos
        servico_pacote_servico_list = ServicoPacoteServico.objects.select_related('servico').filter(pacote_servico=pacote)
        for servico_contido_pacote in servico_pacote_servico_list:
            #  cria cada servico contido no pacote como uma prestacao de servico nao agendada
            PrestacaoServicoPacote.objects.create(cliente=cliente,
                                                  pacoteServico_cliente=pacote_cliente,
                                                  servico_pacoteservico=servico_contido_pacote,
                                                  status=StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.NAO_AGENDADO),
                                                  discriminator=PrestacaoServico.PACOTE,
                                                  recepcionista=recepcionista,
                                                  )
        pacote_cliente.cliente.atualiza_visto_em_agora()
        return pacote_cliente

    def _get_servico_object(self):
        "Retorna o servico prestado de acordo com o tipo de PrestacaoServico(Servico|Pacote)"
        if self.discriminator == PrestacaoServico.PACOTE:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoPacote.objects.get(id=self.id)

            return self.obj_filho.servico_pacoteservico.servico
        elif self.discriminator == PrestacaoServico.SERVICO:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoServico.objects.get(id=self.id)

            return self.obj_filho.servico
        else:
            return None

    servico_object = property(_get_servico_object)

    def _get_servico_prestado(self):
        "Retorna o servico prestado de acordo com o tipo de PrestacaoServico(Servico|Pacote)"
        retorno = self._get_servico_object()
        if retorno:
            return '%s' % (retorno.nome)
        else:
            return 'ops, isso nao deveria aparecer'

    servico_prestado = property(_get_servico_prestado)

    def _get_pacote_servico(self):
        "Retorna o pacote de servico se pacote, senao retorna - "
        if self.discriminator == PrestacaoServico.PACOTE:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoPacote.objects.get(id=self.id)

            return '%s' % (self.obj_filho.servico_pacoteservico.pacote_servico.nome)
        elif self.discriminator == PrestacaoServico.SERVICO:
            return 'Avulso'
        else:
            return 'ops, isso nao deveria aparecer'

    pacote_servico = property(_get_pacote_servico)

    def _get_pago(self):
        "Retorna o pacote de servico se pacote, senao retorna - "
        if self.discriminator == PrestacaoServico.PACOTE:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoPacote.objects.get(id=self.id)

            return '%s' % ("Sim" if self.obj_filho.pacoteServico_cliente.pagamento != None else "Nao")
        elif self.discriminator == PrestacaoServico.SERVICO:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoServico.objects.get(id=self.id)

            return '%s' % ("Sim" if self.obj_filho.pagamento != None else "Nao")
        else:
            return 'ops, isso nao deveria aparecer'

    pago = property(_get_pago)

    def _get_cliente_object(self):
        "Retorna o cliente "
        if self.discriminator == PrestacaoServico.PACOTE:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoPacote.objects.get(id=self.id)

            return self.obj_filho.pacoteServico_cliente.cliente

        elif self.discriminator == PrestacaoServico.SERVICO:
            if self.obj_filho is None:
                self.obj_filho = PrestacaoServicoServico.objects.get(id=self.id)

            return self.obj_filho.cliente
        else:
            return None

    cliente_object = property(_get_cliente_object)

    def _get_cliente(self):
        "Retorna o cliente "
        retorno = self._get_cliente_object()
        if retorno:
            return '%s' % (retorno.nome)
        else:
            return 'ops, isso nao deveria aparecer'

    cliente = property(_get_cliente)

    def __unicode__(self):
        return "[%s] %s"% (self.discriminator, self.status.descricao_curta)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PrestacaoServicoPacote(PrestacaoServico):
    """
    Armazena as prestaoes de servicos
    """
    class Meta:
        verbose_name = 'Prestacao Servico de Pacote'
        verbose_name_plural = 'Prestacoes de Servicos de Pacotes'

    servico_pacoteservico = models.ForeignKey(ServicoPacoteServico)
    pacoteServico_cliente = models.ForeignKey(PacoteServicoCliente)

    def __unicode__(self):
        return "%s %s" % (self.servico_pacoteservico.servico.nome, self.pacoteServico_cliente.cliente.nome)

    def get_absolute_url(self, return_type=None):
        return generic_get_absolute_url(self, return_type)

class PrestacaoServicoServico(PrestacaoServico):
    """
    Armazena as prestaoes de servicos
    """
    class Meta:
        verbose_name = 'Prestacao Servico Simples'
        verbose_name_plural = 'Prestacoes de Servicos Simples'

    cliente = models.ForeignKey(Cliente)
    servico = models.ForeignKey(Servico)
    pagamento = models.ForeignKey('Pagamento', null=True, blank=True)

    def _get_realizado(self):
        return self.status == StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.REALIZADO)

    realizado = property(_get_realizado)

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
