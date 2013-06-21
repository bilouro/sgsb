# -*- coding: UTF-8 -*-
from datetime import timedelta
from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class RelatorioRecebimento(FormView):
    class BuscaForm(forms.Form):
        recebido_por = forms.ModelMultipleChoiceField(queryset=Funcionario.objects.all(), required=False)
        cliente = forms.ModelMultipleChoiceField(queryset=Cliente.objects.all(), required=False)
        de = forms.DateField(widget=widgets.AdminDateWidget, required=False, initial=timezone.datetime.today())
        ate = forms.DateField( widget=widgets.AdminDateWidget, required=False, initial=timezone.datetime.today())
        forma_pagamento = forms.ModelMultipleChoiceField(queryset=FormaPagamento.objects.all(), required=False)
        valor_maior_que = forms.DecimalField( max_digits=7, decimal_places=2, required=False )
        valor_menor_que = forms.DecimalField( max_digits=7, decimal_places=2, required=False )
        imprime_filtro = forms.BooleanField(initial=True, required=False)

    template_name = 'cadastro/cbv/relatoriorecebimentofiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #busca todos os funcionarios
        object_list = Pagamento.objects.all()

        if form.cleaned_data['recebido_por']:
            object_list = object_list.filter(recepcionista__in=form.cleaned_data['recebido_por'])
        if form.cleaned_data['cliente']:
            object_list = object_list.filter(cliente__in=form.cleaned_data['cliente'])
        if form.cleaned_data['de']:
            object_list = object_list.filter(data_hora__gte=form.cleaned_data['de'])
        if form.cleaned_data['ate']:
            um_dia = timedelta(days=1)
            object_list = object_list.filter(data_hora__lt=form.cleaned_data['ate']+um_dia)
        if form.cleaned_data['forma_pagamento']:
            object_list = object_list.filter(forma_pagamento__in=form.cleaned_data['forma_pagamento'])
        if form.cleaned_data['valor_maior_que']:
            object_list = object_list.filter(valor__gte=form.cleaned_data['valor_maior_que'])
        if form.cleaned_data['valor_menor_que']:
            object_list = object_list.filter(valor__lte=form.cleaned_data['valor_menor_que'])

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatoriorecebimentoresultado.html', {
            'form': form,
            'object_list':object_list.order_by('-data_hora'),
            'now': timezone.datetime.now(),
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))
