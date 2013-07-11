# -*- coding: UTF-8 -*-
import calendar
import datetime
from django import forms
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
import itertools
from cadastro.models import *
from django.contrib import messages


from django.contrib.admin import widgets

class HorarioDisponivelFuncionarioGerar(FormView):
    class HorarioDisponivelFuncionarioGerarForm(forms.Form):
        GERAR_MESES = (
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
        GERAR_ANOS =  ( (timezone.datetime.today().year+y, str(timezone.datetime.today().year+y)) for y in range(2) )
        meses = forms.MultipleChoiceField(required=True, choices=GERAR_MESES, initial=[timezone.datetime.today().month+1])
        ano = forms.ChoiceField(required=True, choices=GERAR_ANOS, initial=timezone.datetime.today().year)
        func_list = Funcionario.objects.filter( id__in = EspecialidadeFuncionario.objects.all().values_list('funcionario__id', flat=True).distinct())
        funcionarios = forms.ModelMultipleChoiceField(
            queryset=func_list,
            required=True,
            initial=func_list,
            widget=forms.SelectMultiple(attrs={'style':"height: 130px"}))

        def clean(self):
            cleaned_data = super(HorarioDisponivelFuncionarioGerar.HorarioDisponivelFuncionarioGerarForm, self).clean()
            ano=int(cleaned_data['ano'])
            mes_list=cleaned_data['meses']
            for mes_str in mes_list:
                mes = int(mes_str)
                hdf = HorarioDisponivelFuncionario.objects.filter(data__year=ano).filter(data__month=mes)
                if cleaned_data.get('funcionarios', None):
                    hdf = hdf.filter(funcionario__in=cleaned_data['funcionarios'])
                if hdf.count() > 0:
                    raise forms.ValidationError("Ja existe horario gerado para a combinacao mes/ano/funcionario.")

            return cleaned_data


    template_name = 'cadastro/cbv/horario_disponivel_funcionario_gerar.html'
    form_class = HorarioDisponivelFuncionarioGerarForm
    success_url = '/admin/cadastro/horariodisponivelfuncionario/'

    @transaction.commit_on_success
    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        ano=int(form.cleaned_data['ano'])
        mes_list=form.cleaned_data['meses']
        funcionario_com_especialidade_list=form.cleaned_data['funcionarios']
        mes = None
        for mes_str in mes_list:
            mes = int(mes_str)
            ret_code = HorarioDisponivelFuncionario.gerar_mes(ano=ano, funcionario_list=funcionario_com_especialidade_list, mes=mes)
            if ret_code == HorarioDisponivelFuncionario.GERAR_SUCESSO:
                messages.add_message(self.request, messages.SUCCESS, 'Gerado com sucesso para %s/%s.' % (mes, ano))
            elif ret_code == HorarioDisponivelFuncionario.GERAR_ERRO_HORARIO:
                messages.add_message(self.request, messages.ERROR, 'Ja existe horario gerado para a combinacao mes/ano/funcionario.')
                return HttpResponseRedirect('/cadastro/horariodisponivelfuncionario/gerar')

        return HttpResponseRedirect(self.get_success_url()+'?data__year=%s&data__month=%s' % (ano, mes) )

    #verificar se o form eh valido ok, depois tem q devolver ele com outros horarios. se tiver por exemplo a palavra atualiza...