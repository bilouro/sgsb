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

class PrestacaoServicoPagamentoList(FormView):

    class CustomForm(forms.Form):
        qs=Cliente.objects.all().order_by('-visto_em')
        cliente = forms.ModelChoiceField(queryset=qs, initial=qs[0] if len(qs)>0 else None)

    class FormaPagamentoForm(CustomForm):
        qs=FormaPagamento.objects.all()
        forma_pagamento = forms.ModelChoiceField(queryset=qs, required=True, initial=qs[0] if len(qs)>0 else None)
        valor_pago = forms.DecimalField(decimal_places=2, max_digits=7, widget=forms.HiddenInput(), initial=0)

    class CheckBoxForm(FormaPagamentoForm):
        pss = forms.ModelMultipleChoiceField(queryset=PrestacaoServicoServico.objects.all(), required=False)
        psc = forms.ModelMultipleChoiceField(queryset=PacoteServicoCliente.objects.all(), required=False)

    template_name = 'cadastro/cbv/prestacao_servico_pagamento_list.html'
    form_class = CustomForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def busca_servicos_a_pagar(self, cliente):
        pss = PrestacaoServicoServico.objects.filter(pagamento__isnull=True).filter(cliente=cliente)
        psc = PacoteServicoCliente.objects.filter(pagamento__isnull=True).filter(cliente=cliente)
        return pss, psc

    def get_context_data(self, **kwargs):
        #busca o contexto gerado pela classe superior
        context = super(PrestacaoServicoPagamentoList, self).get_context_data(**kwargs)
        form = kwargs['form']
        cliente = form.fields['cliente'].initial
        if cliente is None:
            return context

        #form com forma de pagamento
        context['form'] = PrestacaoServicoPagamentoList.FormaPagamentoForm(initial=form.initial)

        #busca a prestacao de servico do banco
        pss_list, psc_list = self.busca_servicos_a_pagar(cliente)

        #adiciona o cliente o servico e o id da prestacao
        context['pss_list']=pss_list
        context['psc_list']=psc_list
        return context

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        cliente = form.cleaned_data['cliente']

        if self.request.POST.get('Pagar', None):
            form = PrestacaoServicoPagamentoList.CheckBoxForm(form.data)
            if form.is_valid():
                #busca todas as dependencias para salvar
                pss_selected_list = form.cleaned_data['pss']
                psc_selected_list = form.cleaned_data['psc']
                forma_pagamento = form.cleaned_data['forma_pagamento']
                valor_pago = form.cleaned_data['valor_pago']
                recepcionista = UserProfile.objects.get(user=self.request.user).perfil_funcionario

                with transaction.commit_on_success():
                    #chama metodo de negocio
                    ret_code = Pagamento.realiza_pagamento(cliente, forma_pagamento, recepcionista, pss_selected_list, psc_selected_list, valor_pago)
                #avalia retorno
                if ret_code == Pagamento.REALIZAR_PAGAMENTO_SUCESSO:
                    messages.add_message(self.request, messages.SUCCESS, 'Pagamento efetuado para %s: R$ %.2f %s' % (cliente, valor_pago, forma_pagamento))
                elif ret_code == Pagamento.REALIZAR_PAGAMENTO_ERRO_VALOR:
                    messages.add_message(self.request, messages.ERROR, 'Houve divergencia nos valores, pagamento nao realizado')

                form = PrestacaoServicoPagamentoList.FormaPagamentoForm(initial={'cliente':cliente, 'valor_pago':0})
        else:
            if self.request.POST.get('Buscar', None):
                form = PrestacaoServicoPagamentoList.CheckBoxForm(form.data)
                if form.is_valid():
                    #busca todas as dependencias para salvar
                    pss_selected_list = form.cleaned_data['pss']
                    psc_selected_list = form.cleaned_data['psc']
            else:
                form = PrestacaoServicoPagamentoList.FormaPagamentoForm(initial=form.data)

        #busca as listas de servicos a pagar no banco
        pss_list, psc_list = self.busca_servicos_a_pagar(cliente)

        #chama o template resultado enviando o form, as listas,
        return render_to_response('cadastro/cbv/prestacao_servico_pagamento_list.html', {
            'form': form,
            'pss_list': pss_list,
            'psc_list': psc_list,
            'pss_selected_list': pss_selected_list or None,
            'psc_selected_list': psc_selected_list or None,
        }, context_instance=RequestContext(self.request))
