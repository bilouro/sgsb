# -*- coding: UTF-8 -*-
from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class RelatorioClienteFiltro(FormView):
    class BuscaForm(forms.Form):
        MESES_DO_ANO = (
                (1, 'Janeiro'),
                (2, 'Fevereiro'),
                (3, 'Marco'),
                (4, 'Abril'),
                (5, 'Maio'),
                (6, 'Junho'),
                (7, 'Julho'),
                (8, 'Agosto'),
                (9, 'Setembro'),
                (10, 'Outubro'),
                (11, 'Novembro'),
                (12, 'Dezembro'),
            )
        ULTIMO_CONTATO = (
                (0, '---'),
                (7, '7 dias'),
                (15, '15 dias'),
                (30, '1 mes'),
                (45, '45 dias'),
                (60, '2 meses'),
                (90, '3 meses'),
                (180, '6 meses'),
                (360, '1 ano'),
                (720, '2 anos'),
                (1080, '3 anos'),
                (1440, '4 anos'),
            )
        cadastrado_de = forms.DateField(widget=widgets.AdminDateWidget, required=False)
        cadastrado_ate = forms.DateField( widget=widgets.AdminDateWidget, required=False)
        aniversaria_em = forms.MultipleChoiceField(required=False, choices=MESES_DO_ANO)
        status = forms.ModelMultipleChoiceField(queryset=StatusCliente.objects.all(), initial=[1,])
        ultimo_contato_a_mais_de = forms.ChoiceField(required=False, choices=ULTIMO_CONTATO)
        imprime_filtro = forms.BooleanField(initial=True, required=False)

    template_name = 'cadastro/cbv/relatorioclientesfiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #busca todos os clientes
        cliente_list = Cliente.objects.all()

        if form.cleaned_data['cadastrado_de']:
            #se prencheu dt_cadastro entao busta todas os cadastros maiores(greater than) ou iguais(equal) a data digitada(gte)
            cliente_list = cliente_list.filter(data_cadastro__gte=form.cleaned_data['cadastrado_de'])

        if form.cleaned_data['cadastrado_ate']:
            #se prencheu dt_cadastro entao busta todas os cadastros menores(less than) ou iguais(equal) a data digitada(lte)
            cliente_list = cliente_list.filter(data_cadastro__lte=form.cleaned_data['cadastrado_ate'])

        if form.cleaned_data['aniversaria_em']:
            #se prencheu mes de aniversario
            mes_aniversaria_em_list = []
            #lista os meses escolhidos
            for mes in form.cleaned_data['aniversaria_em']:
                mes_aniversaria_em_list.append(Q(data_nascimento__month=mes))
            if mes_aniversaria_em_list:
                from operator import __or__ as OR
                #filtra and (mes.month =1 OR mes.month=2 ...)
                cliente_list = cliente_list.filter(reduce(OR, mes_aniversaria_em_list))

        if form.cleaned_data['status']:
            #se prencheu status busca tosdos clientes com os status in (1,2)
            cliente_list = cliente_list.filter(status__in=form.cleaned_data['status'])

        if form.cleaned_data['ultimo_contato_a_mais_de']:
            #se prencheu ultimo_contato_a_mais_de
            from datetime import datetime, timedelta
            #cria o delta de X dias
            a_mais_de=timedelta(days=int(form.cleaned_data['ultimo_contato_a_mais_de']))
            #diminui AGORA o valor de dias escolhido em ultimo_contato_a_mais_de
            #se o campo visto_em for MENOR que AGORA(20/05/13 AS 22:30)-7 DIAS
            #significa q foi visto a menos que 7 dias.
            cliente_list = cliente_list.filter(visto_em__lt=datetime.now()-a_mais_de)

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatorioclientesresultado.html', {
            'form': form,
            'object_list':cliente_list,
            'now': timezone.datetime.now(),
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))
