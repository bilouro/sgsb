from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class RelatorioFuncionarioFiltro(FormView):
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
        admissao_de = forms.DateField(widget=widgets.AdminDateWidget, required=False)
        admissao_ate = forms.DateField( widget=widgets.AdminDateWidget, required=False)
        aniversaria_em = forms.MultipleChoiceField(required=False, choices=MESES_DO_ANO)
        status = forms.ModelMultipleChoiceField(queryset=StatusFuncionario.objects.all(), initial=[1,])
        cargo_list = Cargo.objects.all()
        cargo = forms.ModelMultipleChoiceField(queryset=cargo_list, initial=cargo_list)
        imprime_filtro = forms.BooleanField(initial=True, required=False)

    template_name = 'cadastro/cbv/relatoriofuncionariosfiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #busca todos os funcionarios
        funcionario_list = Funcionario.objects.all()

        if form.cleaned_data['admissao_de']:
            #se prencheu admissao_de entao busta todas as admissoes maiores(greater than) ou iguais(equal) a data digitada(gte)
            funcionario_list = funcionario_list.filter(data_admissao__gte=form.cleaned_data['admissao_de'])

        if form.cleaned_data['admissao_ate']:
            #se prencheu admissao_de entao busta todas as admissoes menores(less than) ou iguais(equal) a data digitada(lte)
            funcionario_list = funcionario_list.filter(data_admissao__lte=form.cleaned_data['admissao_ate'])

        if form.cleaned_data['aniversaria_em']:
            #se prencheu mes de aniversario
            mes_aniversaria_em_list = []
            #lista os meses escolhidos
            for mes in form.cleaned_data['aniversaria_em']:
                mes_aniversaria_em_list.append(Q(data_nascimento__month=mes))
            if mes_aniversaria_em_list:
                from operator import __or__ as OR
                #filtra and (mes.month =1 OR mes.month=2 ...)
                funcionario_list = funcionario_list.filter(reduce(OR, mes_aniversaria_em_list))

        if form.cleaned_data['status']:
            #se prencheu status busca tosdos funcionarios com os status in (1,2)
            funcionario_list = funcionario_list.filter(status__in=form.cleaned_data['status'])

        if form.cleaned_data['cargo']:
            #se prencheu cargo busca tosdos funcionarios com os cargos in (1,2)
            funcionario_list = funcionario_list.filter(cargo__in=form.cleaned_data['cargo'])

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatoriofuncionariosresultado.html', {
            'form': form,
            'object_list':funcionario_list,
            'now': timezone.datetime.now(),
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))
