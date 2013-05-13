from django.conf.urls import *
from django.contrib.auth.views import login, logout
from views import PrestacaoServicoListView
from cbv.relatoriofuncionarios import RelatorioFuncionarioView

urlpatterns = patterns('',
     (r'^$', 'cadastro.views.index'),
     (r'^entrar/$', 'django.contrib.auth.views.login', {'template_name': 'entrar.html'}, 'entrar'),
     (r'^sair/$', 'django.contrib.auth.views.logout', {'template_name': 'sair.html'}, 'sair'),
     url(r'^servicos/$', PrestacaoServicoListView.as_view(), name='prestacaoservico-list'),
     url(r'^relatorio/funcionario$', RelatorioFuncionarioView.as_view(), name='relatorio-funcionario'),

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