from django.conf.urls import *
from django.contrib.auth.views import login, logout
from cadastro.cbv.prestacaoservico_agendar import PrestacaoServicoAgendar
from cadastro.cbv.prestacaoservico_novo import PrestacaoServicoNovo
from cadastro.cbv.relatorioclientes import RelatorioClienteFiltro
from views import PrestacaoServicoListView
from cbv.relatoriofuncionarios import RelatorioFuncionarioFiltro

urlpatterns = patterns('',
     (r'^$', 'cadastro.views.index'),
     (r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'entrar.html'}, 'entrar'),
     (r'^sair/$', 'django.contrib.auth.views.logout', {'template_name': 'sair.html'}, 'sair'),
     url(r'^servicos/$', PrestacaoServicoListView.as_view(), name='prestacaoservico-list'),
     url(r'^relatorio/funcionario$', RelatorioFuncionarioFiltro.as_view(), name='relatorio-funcionario'),
     url(r'^prestacaoservico/novo$', PrestacaoServicoNovo.as_view(), name='prestacao-servico-add'),
     url(r'^prestacaoservico/(?P<instance_id>\d+)/agendar$', PrestacaoServicoAgendar.as_view(), name='prestacao-servico-agendar'),
     url(r'^relatorio/cliente$', RelatorioClienteFiltro.as_view(), name='relatorio-cliente'),

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