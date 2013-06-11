# -*- coding: UTF-8 -*-
from django import forms
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.base import RedirectView, View
from django.views.generic.edit import FormView

from cadastro.models import *
from django.contrib import messages


from django.contrib.admin import widgets

class ClientePagamentoCancelar(View):

    @transaction.commit_on_success
    def dispatch(self, request, *args, **kwargs):
        #busca o id da prestacao passado na url
        pagamento_id = kwargs['instance_id']
        cliente_id = kwargs['cliente_id']
        with transaction.commit_on_success():
            # This code executes inside a transaction.
           ret_code = Pagamento.cancelar_pagamento(pagamento_id)
        if ret_code == Pagamento.CANCELAR_PAGAMENTO_SUCESSO:
            messages.add_message(request, messages.SUCCESS, 'Pagamento cancelado com sucesso!')
        elif ret_code == Pagamento.CANCELAR_PAGAMENTO_ERRO_PAGAMENTO_NAO_EXISTE:
            messages.add_message(request, messages.ERROR, 'Pagamento já foi cancelado!')
        elif ret_code == Pagamento.CANCELAR_PAGAMENTO_ERRO_MAIS_QUE_UM:
            messages.add_message(request, messages.ERROR, 'Ops, isso não deveria acontecer. Tem mais de um pagmento com memo número!')
        elif ret_code == Pagamento.CANCELAR_PAGAMENTO_ERRO_NENHUM_ITEM:
            messages.add_message(request, messages.ERROR, 'Ops, Esse pagamento não tem nenhum item?!')
        else:
            messages.add_message(messages.ERROR, 'Ops, algo errado aconteceu...')

        return redirect('/cadastro/cliente/%s/pagamento/historico?q=%s' % (cliente_id, timezone.datetime.now().microsecond) )