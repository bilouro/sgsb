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

class RelatorioComissao(FormView):
    class BuscaForm(forms.Form):
        today = timezone.datetime.today()
        primeiro_dia_mes = datetime.date(today.year, today.month, 1)
        ultimo_dia_mes = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        prestador_list = Funcionario.objects.filter( id__in = EspecialidadeFuncionario.objects.all().values_list('funcionario__id', flat=True).distinct())
        prestadores = forms.ModelMultipleChoiceField(queryset=prestador_list, required=False)
        de = forms.DateField(widget=widgets.AdminDateWidget, required=False, initial=primeiro_dia_mes)
        ate = forms.DateField( widget=widgets.AdminDateWidget, required=False, initial=ultimo_dia_mes)
        imprime_filtro = forms.BooleanField(initial=True, required=False)

    template_name = 'cadastro/cbv/relatoriocomissaofiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #busca todos os funcionarios
        object_list = PrestacaoServico.objects.filter(status=StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.REALIZADO))

        if form.cleaned_data['de']:
            object_list = object_list.filter(horario__data__gte=form.cleaned_data['de'])
        if form.cleaned_data['ate']:
            object_list = object_list.filter(horario__data__lte=form.cleaned_data['ate'])
        if form.cleaned_data['prestadores']:
            object_list = object_list.filter(horario__funcionario__in=form.cleaned_data['prestadores'])

        #contagem de objetos
        object_count = object_list.count()
        valor_geral = [0,0]

        #identifica os prestadores exitentes na lista de prestacoes
        prestadores_distintos = object_list.values_list('horario__funcionario', flat=True).distinct()

        #separa as prestacoes por prestador
        #acumula os valores
        prestacoes_por_prestador = {}
        for prestador_id in prestadores_distintos:

            prestacao_prestador_list = object_list.filter(horario__funcionario__id=prestador_id).order_by('horario__data')
            prestador = prestacao_prestador_list[0].horario.funcionario

            prestacoes_por_prestador[prestador] = [0, 0, prestacao_prestador_list]
            for p in prestacao_prestador_list:
                prestacoes_por_prestador[prestador][0] += p.valor
                prestacoes_por_prestador[prestador][1] += p.comissao
                #totalizadores gerais
                valor_geral[0] += p.valor
                valor_geral[1] += p.comissao

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatoriocomissaoresultado.html', {
            'form': form,
            'object_list':prestacoes_por_prestador,
            'now': timezone.datetime.now(),
            'object_count':object_count,
            'valor_geral':valor_geral,
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))
