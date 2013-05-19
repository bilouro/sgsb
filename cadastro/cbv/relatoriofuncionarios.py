import urllib
from django import forms
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
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

    template_name = 'cadastro/cbv/relatoriofuncionariosfiltro.html'
    form_class = BuscaForm
    success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        valores = {}
        valores['admissao_de'] = '' if form.cleaned_data['admissao_de'] == None else form.cleaned_data['admissao_de']
        valores['admissao_ate'] = '' if form.cleaned_data['admissao_ate'] == None else form.cleaned_data['admissao_ate']
        valores['aniversaria_em'] = '-'.join([ ae for ae in form.cleaned_data['aniversaria_em'] ])
        valores['status'] = '-'.join([ str(s.pk) for s in form.cleaned_data['status'] ])
        valores['cargo'] = '-'.join([ str(c.pk) for c in form.cleaned_data['cargo'] ])

        return HttpResponseRedirect(self.get_success_url() + '?' + urllib.urlencode(valores))
#        return super(RelatorioFuncionarioFiltro, self).form_valid(form)

class RelatorioFuncionarioResultado(ListView):
    model = Funcionario
    template_name = 'cadastro/cbv/relatoriofuncionariosresultado.html'

    def get_context_data(self, **kwargs):
        context = super(RelatorioFuncionarioResultado, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(RelatorioFuncionarioResultado, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super(RelatorioFuncionarioResultado, self).get_queryset()
        return queryset

    def get(self, request, *args, **kwargs):
        return super(RelatorioFuncionarioResultado, self).get(request, *args, **kwargs)
