from django import forms
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import FormView
RedirectView

from cadastro.models import *
from django.contrib import messages

class PrestacaoServicoRealizar(View):

    @transaction.commit_on_success
    def dispatch(self, request, *args, **kwargs):
        #busca o id da prestacao passado na url
        prestacao_servico_id = kwargs['instance_id']
        #busca a prestacao de servico do banco
        prestacao_servico = get_object_or_404(PrestacaoServico, id=prestacao_servico_id)

        with transaction.commit_on_success():
            # This code executes inside a transaction.
            ret_code = PrestacaoServico.realizar(prestacao_servico)
        if ret_code == PrestacaoServico.REALIZAR_SUCESSO:
            messages.add_message(request, messages.SUCCESS, 'Realizado com sucesso!')
        elif ret_code == PrestacaoServico.REALIZAR_ERRO_PRESTACAO:
            messages.add_message(request, messages.ERROR, 'Para realizar o servico ele deve estar com o status %s.' % StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.AGENDADO))
        else:
            messages.add_message(messages.ERROR, 'Ops, algo errado aconteceu...')

        return redirect(self.get_success_url()+'?cliente=%s' % prestacao_servico.cliente_object.id)

    def get_success_url(self):
        return '/admin/cadastro/prestacaoservico'
