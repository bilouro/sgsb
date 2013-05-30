from django import forms
from django.db import transaction
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *
from django.contrib import messages


from django.contrib.admin import widgets

class PrestacaoServicoAgendar(FormView):
    class PrestacaoServicoAgendarForm(forms.Form):
        funcionario = forms.ModelChoiceField(required=True, queryset=Funcionario.objects.all())
        data = forms.DateField(widget=widgets.AdminDateWidget, required=True, initial=timezone.datetime.today())
        horario = forms.ModelChoiceField(queryset=HorarioDisponivelFuncionario.objects.all(), widget=forms.RadioSelect, required=False)

    template_name = 'cadastro/cbv/prestacao_servico_agendar.html'
    form_class = PrestacaoServicoAgendarForm
    success_url = '/admin/cadastro/prestacaoservico'

    def prepara_form(self, data, form, funcionario, prestacao_servico):
        #busca a lista de funcionarios com a especialidade do servico escolhido e que estejam habilitados
        funcionario_id_list = EspecialidadeFuncionario.objects.filter(
            especialidade=prestacao_servico.servico_object.especialidade).filter(
            funcionario__status__habilitado=True).values_list('funcionario__id', flat=True)
        funcionario_list = Funcionario.objects.filter(id__in=funcionario_id_list)

        if funcionario is None and len(funcionario_list)==1:
            funcionario = funcionario_list[0]

        form.fields['funcionario'] = forms.ModelChoiceField(required=True, queryset=funcionario_list,
                                                            initial=funcionario)
        if funcionario is None:
            qs = HorarioDisponivelFuncionario.objects.get_empty_query_set()
            form.fields['horario'] = forms.ModelChoiceField(queryset=qs, required=True)

            messages.add_message(self.request, messages.INFO, 'Selecione um funcionario')
        else:
            qs = HorarioDisponivelFuncionario.objects \
                .filter(funcionario=funcionario) \
                .filter(data=data) \
                .filter(disponivel=True)
            form.fields['horario'] = forms.ModelChoiceField(queryset=qs, required=True)

            messages.add_message(self.request, messages.INFO, 'Exibindo dia %s de %s' % (data.strftime("%d/%m/%Y"),
                                                                                             funcionario.nome))

    def get_context_data(self, **kwargs):
        #busca o id da prestacao passado na url
        prestacao_servico_id = self.kwargs['instance_id']

        #busca a prestacao de servico do banco
        prestacao_servico = get_object_or_404(PrestacaoServico, id=prestacao_servico_id)

        #busca o cliente
        cliente = prestacao_servico.cliente_object

        #busca o servico envolvido
        servico = prestacao_servico.servico_object

        form = kwargs['form']
        self.prepara_form(form.fields['data'].initial,form, None, prestacao_servico)

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
        #buscando  dados do form
        #busca o id da prestacao passado na url
        prestacao_servico_id = self.kwargs['instance_id']
        #busca a prestacao de servico do banco
        prestacao_servico = get_object_or_404(PrestacaoServico, id=prestacao_servico_id)

        if self.request.POST.get('Atualizar',None):
            self.prepara_form(form.cleaned_data['data'], form, form.cleaned_data['funcionario'], prestacao_servico)
            return render_to_response(self.template_name, {
                'form': form,
                'cliente':prestacao_servico.cliente_object,
                'servico':prestacao_servico.servico_object,
                'prestacao_servico_id':prestacao_servico_id,
            }, context_instance=RequestContext(self.request))

        if self.request.POST.get('Agendar',None):
            #se nao eh um refresh entao salva
            #chama metodo de negocio para agendar prestacao_servico
            horario_funcionario = form.cleaned_data['horario']

            with transaction.commit_on_success():
                # This code executes inside a transaction.
                ret_code = PrestacaoServico.agendar(horario_funcionario=horario_funcionario, prestacao_servico=prestacao_servico)
            if ret_code == PrestacaoServico.AGENDAR_SUCESSO:
                messages.add_message(self.request, messages.SUCCESS, 'Agendado com %s dia %s as %s' % (horario_funcionario.funcionario, horario_funcionario.data.strftime("%d/%m/%Y"), horario_funcionario.hora.hora.strftime('%H:%M')))
            elif ret_code == PrestacaoServico.AGENDAR_ERRO_HORARIO:
                messages.add_message(self.request, messages.ERROR, 'O horario: "%s" nao esta mais disponivel.' % horario_funcionario)
            elif ret_code == PrestacaoServico.AGENDAR_ERRO_PRESTACAO:
                messages.add_message(self.request, messages.ERROR, 'Para agendar o servico ele deve estar com o status %s.' % StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.NAO_AGENDADO))
            else:
                messages.add_message(self.request, messages.ERROR, 'Ops, algo errado aconteceu...')
            return HttpResponseRedirect(self.get_success_url()+'?cliente=%s' % prestacao_servico.cliente_object.id)

        messages.add_message(self.request, messages.INFO, 'Nada alterado')
        return HttpResponseRedirect(self.get_success_url())

    #verificar se o form eh valido ok, depois tem q devolver ele com outros horarios. se tiver por exemplo a palavra atualiza...