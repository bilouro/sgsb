# -*- coding: UTF-8 -*-
from django import forms
from django.db import transaction
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets
from django.contrib import messages

class ClientePagamentoHistorico(FormView):

    class CustomForm(forms.Form):
        cliente = forms.ModelChoiceField(queryset=Cliente.objects.all())

    template_name = 'cadastro/cbv/cliente_pagamento_historico.html'
    form_class = CustomForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def busca_pagamentos_efetuados(self, cliente):
        return Pagamento.objects.filter(cliente=cliente)

    def get_context_data(self, **kwargs):
        #busca o contexto gerado pela classe superior
        context = super(ClientePagamentoHistorico, self).get_context_data(**kwargs)

        #form
        cliente = get_object_or_404(Cliente, id=self.kwargs['instance_id'])
        context['form'] = ClientePagamentoHistorico.CustomForm(initial={'cliente':cliente })

        #busca pagamentos efetuados
        context['object_list']=self.busca_pagamentos_efetuados(cliente)
        return context

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        return render_to_response(self.template_name, {
            'form': form,
            'object_list': self.busca_pagamentos_efetuados( form.cleaned_data['cliente'] )
        }, context_instance=RequestContext(self.request))

