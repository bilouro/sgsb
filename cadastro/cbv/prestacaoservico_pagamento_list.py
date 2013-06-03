from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class PrestacaoServicoPagamentoList(FormView):

    class CustomForm(forms.Form):
        qs=Cliente.objects.all().order_by('-visto_em')
        cliente = forms.ModelChoiceField(queryset=qs, initial=qs[0] if len(qs)>0 else None)

    template_name = 'cadastro/cbv/prestacao_servico_pagamento_list.html'
    form_class = CustomForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def get_context_data(self, **kwargs):
        #busca o contexto gerado pela classe superior
        context = super(PrestacaoServicoPagamentoList, self).get_context_data(**kwargs)
        form = kwargs['form']
        cliente = form.fields['cliente'].initial
        if cliente is None:
            return context

        #busca a prestacao de servico do banco
        pss_list = PrestacaoServicoServico.objects.filter(pagamento__isnull=True).filter(cliente=cliente)
        psc_list = PacoteServicoCliente.objects.filter(pagamento__isnull=True).filter(cliente=cliente)

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
        #busca todos os funcionarios
        #funcionario_list = Funcionario.objects.all()

        # if form.cleaned_data['admissao_de']:
        #     #se prencheu admissao_de entao busta todas as admissoes maiores(greater than) ou iguais(equal) a data digitada(gte)
        #     funcionario_list = funcionario_list.filter(data_admissao__gte=form.cleaned_data['admissao_de'])

        #busca a prestacao de servico do banco
        pss_list = PrestacaoServicoServico.objects.filter(pagamento__isnull=True).filter(cliente=form.cleaned_data['cliente'])
        psc_list = PacoteServicoCliente.objects.filter(pagamento__isnull=True).filter(cliente=form.cleaned_data['cliente'])

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/prestacao_servico_pagamento_list.html', {
            'form': form,
            'pss_list': pss_list,
            'psc_list': psc_list,
        }, context_instance=RequestContext(self.request))
