# -*- coding: UTF-8 -*-
from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models import Q
from cadastro.models import *
#from cadastro.models import Cliente, Funcionario, UserProfile
from django.utils.html import clean_html


class ClienteAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (('nome', 'data_nascimento'), ('cpf', 'identidade', 'orgao_expedidor'), ('telefone', 'email'), ('logradouro', 'numero'), ('complemento', 'bairro'), ('cidade', 'estado', 'cep'), ('status', 'data_cadastro', 'visto_em'))
        }),
    )
    list_display = ('nome', 'telefone', 'email', 'data_nascimento', 'data_cadastro', 'status')
    date_hierarchy = 'visto_em'
    search_fields = ['nome', 'logradouro', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    list_filter = ['status',]

class PessoaAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', ('logradouro', 'numero'), ('complemento', 'bairro'), ('cidade', 'estado', 'cep'), ('telefone', 'email'), ('cpf', 'identidade', 'orgao_expedidor'), 'data_nascimento')
        }),
    )
    list_display = ('nome', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome', 'logradouro', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    list_filter = ['bairro', 'cidade',]

class DependenteFuncionarioAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Retorna um dict vazio de permissoes que esconde do admin index.
        """
        return {}
    list_display = ('funcionario', 'nome', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome', 'logradouro', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'funcionario__nome'] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    list_filter = ['funcionario',]

class DependenteFuncionarioInline(admin.TabularInline):
    model = DependenteFuncionario
    fk_name = 'funcionario'
    exclude = ('logradouro', 'numero','complemento', 'bairro','cidade', 'estado', 'cep', 'telefone', 'email',)
    extra = 0
class EspecialidadeFuncionarioInline(admin.TabularInline):
    model = EspecialidadeFuncionario
    extra = 1
class FuncionarioAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Dados Pessoais', {
            'fields': (('nome', 'data_nascimento'), ('cpf', 'identidade', 'orgao_expedidor'), ('telefone', 'email'), ('logradouro', 'numero'), ('complemento', 'bairro'), ('cidade', 'estado', 'cep'), ('data_admissao', 'status', 'cargo'))
        }),
    )
    list_display = ('nome', 'telefone', 'email', 'data_admissao', 'status', 'cargo')
    date_hierarchy = 'data_admissao'
    search_fields = ['nome', 'logradouro', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor' ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    inlines = [ DependenteFuncionarioInline, EspecialidadeFuncionarioInline]
    list_filter = ['status','cargo']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','perfil_cliente', 'perfil_funcionario')
    #date_hierarchy = 'dia'
    search_fields = ['user__username','user__first_name', 'user__last_name', 'perfil_cliente__nome', 'perfil_funcionario__nome' ]
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class StatusClienteAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class StatusFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('descricao','habilitado',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    list_filter = ['habilitado',]

class CargoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class EspecialidadeFuncionarioAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Retorna um dict vazio de permissoes que esconde do admin index.
        """
        return {}
    list_display = ('especialidade','funcionario')
    #date_hierarchy = 'data_admissao'
    search_fields = ['especialidade__descricao','funcionario__descricao']
    #ordering = ('-dia',)
    list_filter = ['especialidade','funcionario']


class ServicosPacoteInline(admin.TabularInline):
    model = ServicoPacoteServico
    #fk_name = 'pacote_servico'
    #exclude = ('endereco', 'telefone', 'email',)
    extra = 3
class PacoteServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'valor', 'habilitado')
    search_fields = ['nome', 'descricao', 'valor']
    #ordering = ('-dia',)
    inlines = [ ServicosPacoteInline, ]
    list_filter = ['habilitado']

class ServicoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao', 'valor', 'comissao', 'custo_material', 'especialidade', 'habilitado')
    search_fields = ['nome', 'descricao', 'valor', 'comissao', 'custo_material']
    #ordering = ('-dia',)
    list_filter = ['especialidade','habilitado']

class ServicoPacoteServicoAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Retorna um dict vazio de permissoes que esconde do admin index.
        """
        return {}
    list_display = ('pacote_servico', 'servico', 'valor_rateado')
    search_fields = ['pacote_servico__nome', 'servico__nome', 'valor_rateado']
    #ordering = ('-dia',)
    list_filter = ['pacote_servico',]


class HorarioDisponivelAdmin(admin.ModelAdmin):
    list_display = ('hora', )
    #ordering = ('-dia',)
    #list_filter = ['pacote_servico',]

class HorarioDisponivelFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('data', 'hora', 'funcionario', 'disponivel')
    search_fields = ['funcionario__nome']
    #ordering = ('-dia',)
    list_filter = ['funcionario', 'disponivel','hora__hora']
    date_hierarchy = 'data'


class StatusPrestacaoServicoAdmin(admin.ModelAdmin):
    list_display = ('descricao_curta', 'descricao', 'realizado', 'cancelado')
    search_fields = ['descricao_curta', 'descricao',]
    #ordering = ('-dia',)
    list_filter = ['realizado', 'cancelado']

class PacoteServicoClienteAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'recepcionista', 'pacote_servico', 'pagamento')
    search_fields = ['cliente__nome', 'recepcionista__nome', 'pacote_servico__descricao', 'pacote_servico__nome']
    #ordering = ('-dia',)
    list_filter = ['cliente',]

from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

class ClientesListFilter(SimpleListFilter):
    title = _('top 10 clientes')
    parameter_name = 'cliente'
    def lookups(self, request, model_admin):
        #busca os N clientes mais recentes
        #todo:criar uma tabela de parametros de sistema
        cliente_list = Cliente.objects.all().order_by('-visto_em')[:10]
        return ( (c.id , c.nome) for c in cliente_list )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        #busca todos os servicos SIMPLES do cliente
        pss_id_list = PrestacaoServicoServico.objects.filter(cliente__id=self.value()).values_list('id', flat=True)
        #busca todos os servicos de PACOTE do cliente
        psp_id_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente__cliente__id=self.value()).values_list('id', flat=True)

        return queryset.filter(Q(id__in=pss_id_list) | Q(id__in=psp_id_list))

class PagoListFilter(SimpleListFilter):
    title = _('status pagamento')
    parameter_name = 'pagto'
    def lookups(self, request, model_admin):
        """
        * pagamento isNull == True  -> tras os nao pagos
        * pagamento isNull == False -> tras os pagos
        """
        return ( ("False", 'Pago') , ("True",'Nao Pago') )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        bool_value = (self.value() == "True")

        #busca todos os servicos SIMPLES do cliente
        pss_id_list = PrestacaoServicoServico.objects.filter(pagamento__isnull=bool_value).values_list('id', flat=True)
        #busca todos os servicos de PACOTE do cliente
        psp_id_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente__pagamento__isnull=bool_value).values_list('id', flat=True)

        return queryset.filter(Q(id__in=pss_id_list) | Q(id__in=psp_id_list))

class TipoPrestacaoServicoListFilter(SimpleListFilter):
    title = _('tipo')
    parameter_name = 'tipo'
    def lookups(self, request, model_admin):
        return ( ("SERVICO", 'Apenas Servicos') , ("PACOTE",'Apenas Pacotes') )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(discriminator=self.value())

class PrestacaoServicoAdmin(admin.ModelAdmin):
    usuario = None

    def servico_pacote(self, obj):
        return "%s (%s)" % (obj.servico_prestado , obj.pacote_servico)

    servico_pacote.allow_tags = True
    servico_pacote.short_description = u'Servico (Pacote)'
    #servico_pacote.admin_order_field = 'servico_prestado'

    def funcionario(self, obj):
        return "(nenhum)" if obj.horario is None else "%s" % (obj.horario.funcionario.nome)

    funcionario.allow_tags = True
    funcionario.short_description = u'Funcionario'

    def custom_cliente(self, obj):
        return clean_html("<a href='#'>%s</a>" % obj.cliente)

    custom_cliente.allow_tags = True
    custom_cliente.short_description = u'Cliente'
    custom_cliente.admin_order_field = 'cliente'

    def get_model_perms(self, request):
        """
        SOBRE-ESCRITO PARA BUSCAR O USUARIO DA SESSAO
        """
        global usuario
        usuario = request.user
        return super(PrestacaoServicoAdmin, self).get_model_perms(request)

    def data_hora(self, obj):
        return "(nenhum)" if obj.horario is None else "%s %s" % (obj.horario.data.strftime("%d/%m/%Y"), obj.horario.hora.hora.strftime('%H:%M'))

    data_hora.allow_tags = True
    data_hora.short_description = u'Data e hora'

    def acoes(self, obj):
        cancelar ='<a href="/cadastro/prestacaoservico/%s/cancelar">remover</a>' % obj.id if usuario.has_perm('cadastro.change_funcionario') else ''
        agendar ='<a href="/cadastro/prestacaoservico/%s/agendar">agendar</a>' % obj.id
        desagendar = '<a href="/cadastro/prestacaoservico/%s/desagendar">cancelar</a>' % obj.id
        realizar = '<a href="/cadastro/prestacaoservico/%s/realizar">realizar</a>' % obj.id
        desrealizar = '<a href="/cadastro/prestacaoservico/%s/desrealizar">cancelar</a>' % obj.id if usuario.has_perm('cadastro.change_funcionario') else ''

        workflow = {
            StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.NAO_AGENDADO):" &nbsp; ".join([agendar,cancelar]),
            StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.AGENDADO):" &nbsp; ".join([realizar, desagendar]),
            StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.REALIZADO):" &nbsp; ".join([desrealizar,]),
            StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.CANCELADO):"",
         }
        return workflow[obj.status]

    acoes.allow_tags = True
    acoes.short_description = u'Acoes'

    list_display = ('custom_cliente', 'servico_pacote', 'status', 'data_hora', 'funcionario', 'pago', 'acoes')

    search_fields = []#'horario__funcionario__nome',]#'cliente__nome', 'pacoteServico_cliente__cliente__nome']
    #ordering = ('-dia',)
    #date_hierarchy = 'horario'
    list_filter = ['status', PagoListFilter, TipoPrestacaoServicoListFilter, ClientesListFilter ]

    def queryset(self, request):
        qs = super(PrestacaoServicoAdmin, self).queryset(request)
        query = request.GET.get('q', '')

        #qs = PrestacaoServico.objects.all()
        if query != '':
            #busca todos os servicos SIMPLES do cliente
            pss_id_list = PrestacaoServicoServico.objects.filter(cliente__nome__icontains=query).values_list('id', flat=True)
            #busca todos os servicos de PACOTE do cliente
            psp_id_list = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente__cliente__nome__icontains=query).values_list('id', flat=True)
            qs = qs.filter(Q(id__in=pss_id_list) | Q(id__in=psp_id_list))

        return qs

class PrestacaoServicoPacoteAdmin(admin.ModelAdmin):
    list_display = ('status', 'horario', 'recepcionista', 'servico_pacoteservico', 'pacoteServico_cliente')
    search_fields = ['horario__funcionario__nome', 'servico_pacoteservico__servico__nome', 'pacoteServico_cliente__pacote_servico__nome', 'pacoteServico_cliente__cliente__nome']
    #ordering = ('-dia',)
    #date_hierarchy = 'horario'
    list_filter = ['status']

class PrestacaoServicoServicoAdmin(admin.ModelAdmin):
    list_display = ('status', 'horario', 'recepcionista', 'cliente', 'servico', 'pagamento')
    search_fields = ['horario__funcionario__nome', 'cliente__nome', 'servico__nome']
    list_filter = ['status']

class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    search_fields = ['descricao',]


class PrestacaoServicoInline(admin.TabularInline):
    model = PrestacaoServicoServico
    #fk_name = 'funcionario'
    exclude = ('status', 'horario', 'recepcionista','cliente')
    extra = 0
class PacoteServicoClienteInline(admin.TabularInline):
    model = PacoteServicoCliente
    exclude = ('cliente', 'recepcionista')
    extra = 0

class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'data_hora', 'valor', 'forma_pagamento')
    search_fields = ['cliente__nome','valor', 'forma_pagamento__descricao']
    #ordering = ('-dia',)
    date_hierarchy = 'data_hora'
    list_filter = ['cliente','forma_pagamento']
    inlines = [PacoteServicoClienteInline, PrestacaoServicoInline]

admin.site.register(Pagamento, PagamentoAdmin)
admin.site.register(FormaPagamento, FormaPagamentoAdmin)
admin.site.register(PrestacaoServico, PrestacaoServicoAdmin)
admin.site.register(PrestacaoServicoServico, PrestacaoServicoServicoAdmin)
admin.site.register(PrestacaoServicoPacote, PrestacaoServicoPacoteAdmin)
admin.site.register(PacoteServicoCliente, PacoteServicoClienteAdmin)
admin.site.register(StatusPrestacaoServico, StatusPrestacaoServicoAdmin)
admin.site.register(HorarioDisponivelFuncionario, HorarioDisponivelFuncionarioAdmin)
admin.site.register(HorarioDisponivel, HorarioDisponivelAdmin)
admin.site.register(Servico, ServicoAdmin)
admin.site.register(PacoteServico, PacoteServicoAdmin)
admin.site.register(ServicoPacoteServico, ServicoPacoteServicoAdmin)

admin.site.register(StatusCliente, StatusClienteAdmin)
admin.site.register(StatusFuncionario, StatusFuncionarioAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(DependenteFuncionario, DependenteFuncionarioAdmin)
admin.site.register(EspecialidadeFuncionario,EspecialidadeFuncionarioAdmin )
admin.site.register(Especialidade, EspecialidadeAdmin)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

#modelos uteis do django
admin.site.register(Session)
admin.site.register(Permission)
admin.site.register(ContentType)

