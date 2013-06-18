# -*- coding: UTF-8 -*-
from django.conf.urls import *
from django.contrib.auth.views import login, logout
from django.views.generic.base import TemplateView
from cadastro.cbv.cliente_pagamento_cancelar import ClientePagamentoCancelar
from cadastro.cbv.cliente_pagamento_historico import ClientePagamentoHistorico
from cadastro.cbv.horariodisponivelfuncionario_gerar import HorarioDisponivelFuncionarioGerar
from cadastro.cbv.prestacaoservico_agendar import PrestacaoServicoAgendar
from cadastro.cbv.prestacaoservico_cancelar import PrestacaoServicoCancelar
from cadastro.cbv.prestacaoservico_desagendar import PrestacaoServicoDesagendar
from cadastro.cbv.prestacaoservico_desrealizar import PrestacaoServicoDesrealizar
from cadastro.cbv.prestacaoservico_novo import PrestacaoServicoNovo
from cadastro.cbv.prestacaoservico_pagamento import PrestacaoServicoPagamentoList
from cadastro.cbv.prestacaoservico_realizar import PrestacaoServicoRealizar
from cadastro.cbv.relatorioclientes import RelatorioClienteFiltro
from cadastro.cbv.relatoriopacotependente import RelatorioPacotePendente
from cbv.relatoriofuncionarios import RelatorioFuncionarioFiltro

urlpatterns = patterns('',
     (r'^$', 'cadastro.views.index'),
     (r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'entrar.html'}, 'entrar'),
     (r'^sair/$', 'django.contrib.auth.views.logout', {'template_name': 'sair.html'}, 'sair'),
     url(r'^relatorio/funcionario$', RelatorioFuncionarioFiltro.as_view(), name='relatorio-funcionario'),
     url(r'^prestacaoservico/novo$', PrestacaoServicoNovo.as_view(), name='prestacao-servico-add'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/agendar$', PrestacaoServicoAgendar.as_view(), name='prestacao-servico-agendar'),
     url(r'^relatorio/cliente$', RelatorioClienteFiltro.as_view(), name='relatorio-cliente'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/desagendar$', PrestacaoServicoDesagendar.as_view(), name='prestacao-servico-desagendar'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/realizar$', PrestacaoServicoRealizar.as_view(), name='prestacao-servico-realizar'),
     url(r'^horariodisponivelfuncionario/gerar$', HorarioDisponivelFuncionarioGerar.as_view(), name='horario-disponivel-funcionario-gerar'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/desrealizar$', PrestacaoServicoDesrealizar.as_view(), name='prestacao-servico-desrealizar'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/cancelar$', PrestacaoServicoCancelar.as_view(), name='prestacao-servico-cancelar'),
     url(r'^prestacaoservico/pagamento/$', PrestacaoServicoPagamentoList.as_view(), name='prestacao-servico-pagamento-list'),
     url(r'^cliente/(?P<instance_id>\d+)/pagamento/historico$', ClientePagamentoHistorico.as_view(), name='cliente-pagamento-historico'),
     url(r'^cliente/(?P<cliente_id>\d+)/pagamento/(?P<instance_id>\d+)/cancelar$', ClientePagamentoCancelar.as_view(), name='cliente-pagamento-cancelar'),
     url(r'^relatorios/', TemplateView.as_view(template_name="cadastro/relatorios.html")),
     url(r'^relatorio/pacotependente$', RelatorioPacotePendente.as_view(), name='relatorio-pacote-pendente'),

#    (r'^registrar/$', 'core.views.registrar', {}, 'registrar'),
#    (r'^redefinir/(?P<chave_ativacao>\S+)/$', 'core.views.redefinir'),
#    (r'^esqueci_minha_senha/$', 'core.views.esqueci_minha_senha', {}, 'esqueci_minha_senha'),
    
#    (r'^autocomplete/search/(?P<texto>\S+)$', 'core.views.autocomplete_search'),    
#    (r'^autocomplete/$', 'core.views.autocomplete'),    
#    (r'^usuario/search_ajax/(?P<texto>\S+)$', 'core.views.usuario_search_ajax'),

#    (r'^perfil/(?P<username>\S+)/$', 'core.views.perfil'),
#    (r'^excluir/', 'core.views.excluir'),

#    (r'^desenv/$',               'prototipo.views.index2'),
#    (r'^desenv/relatorios.html', 'prototipo.views.relatorios'),
#    (r'^desenv/caixa_entrada.html','prototipo.views.caixa_entrada'),
#    (r'^relatorio/$','prototipo.views.relatorio'),
)