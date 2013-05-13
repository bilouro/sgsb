from django import forms
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class RelatorioFuncionarioView(FormView):
    class BuscaForm(forms.Form):
        admissao_de = forms.DateField(widget=widgets.AdminDateWidget, required=False)
        admissao_ate = forms.DateField( widget=widgets.AdminDateWidget, required=False)
        aniversario_de = forms.DateField(widget=widgets.AdminDateWidget, required=False)
        aniversario_ate = forms.DateField(widget=widgets.AdminDateWidget, required=False)
        status = forms.ModelMultipleChoiceField(queryset=StatusFuncionario.objects.all(), initial=[1,])
        cargo_list = Cargo.objects.all()
        cargo = forms.ModelMultipleChoiceField(queryset=cargo_list, initial=cargo_list)

        def gera_relatorio(self):
            # gera relatorio self.cleaned_data dictionary
            pass

    template_name = 'cadastro/cbv/relatoriofuncionarios.html'
    form_class = BuscaForm
    success_url = '/thanks/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.gera_relatorio()
        return super(RelatorioFuncionarioView, self).form_valid(form)