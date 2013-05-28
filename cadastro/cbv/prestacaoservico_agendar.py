from django import forms
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class PrestacaoServicoAgendar(FormView):
    class PrestacaoServicoAgendarForm(forms.Form):
        funcionario = forms.ModelChoiceField(required=True, queryset=Funcionario.objects.get_empty_query_set())
        data = forms.DateField(widget=widgets.AdminDateWidget, required=True, initial=timezone.datetime.today())
        horario = forms.ModelChoiceField(queryset=HorarioDisponivelFuncionario.objects.get_empty_query_set(), required=False)

    template_name = 'cadastro/cbv/prestacao_servico_agendar.html'
    form_class = PrestacaoServicoAgendarForm
    success_url = '/admin/cadastro/prestacaoservico'

    def get_context_data(self, **kwargs):
        #busca o id da prestacao passado na url
        prestacao_servico_id = self.kwargs['instance_id']

        #busca a prestacao de servico do banco
        prestacao_servico = get_object_or_404(PrestacaoServico, id=prestacao_servico_id)

        #busca o cliente
        cliente = prestacao_servico.cliente_object

        #busca o servico envolvido
        servico = prestacao_servico.servico_object

        #busca a lista de funcionarios com a especialidade do servico escolhido e que estejam habilitados
        funcionario_id_list = EspecialidadeFuncionario.objects.filter(especialidade=servico.especialidade).filter(funcionario__status__habilitado=True).values_list('funcionario__id', flat=True)
        funcionario_list = Funcionario.objects.filter(id__in=funcionario_id_list)

        #popula o combo funcionario com os funcionarios que tem a especialidade do servico escolhido
        form = kwargs['form']
        form.fields['funcionario'] = forms.ModelChoiceField(required=True, queryset=funcionario_list, initial=funcionario_list[0] if funcionario_list else None)

        #se tiver um funcionario escolhido, preenche os horarios deste funcionario para o dia selecionado
        if form.fields['funcionario'].initial:
            qs = HorarioDisponivelFuncionario.objects.filter(funcionario=form.fields['funcionario'].initial)
            qs = qs.filter(data=form.fields['data'].initial)
            qs = qs.filter(disponivel=True)
            form.fields['horario'] = forms.ModelChoiceField(queryset=qs, required=False)

        #busca o contexto gerado pela classe superior
        context = super(PrestacaoServicoAgendar, self).get_context_data(**kwargs)

        #adiciona o cliente o servico e o id da prestacao
        context['cliente']=cliente
        context['servico']=servico
        context['prestacao_servico_id']=prestacao_servico_id

        return context


    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        from django.contrib import messages
        return super(PrestacaoServicoAgendar, self).form_valid(self, form)

