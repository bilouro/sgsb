from django import forms
from django.db.models.query_utils import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class PrestacaoServicoNovo(FormView):
    class PrestacaoServicoNovoForm(forms.Form):
        cliente = forms.ModelChoiceField(required=True, queryset=Cliente.objects.all())
        servicos = forms.ModelMultipleChoiceField(queryset=Servico.objects.all(), required=False)
        pacote_servicos = forms.ModelMultipleChoiceField(queryset=PacoteServico.objects.all(), required=False)

    template_name = 'cadastro/cbv/prestacao_servico_novo.html'
    form_class = PrestacaoServicoNovoForm
    success_url = '/admin/cadastro/prestacaoservico'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        from django.contrib import messages
        #itera pelos servicos escolhidos
        for servico in form.cleaned_data['servicos']:
            #  cria cada servico contido na lista como uma prestacao de servico nao agendada para o cliente escolhido
            PrestacaoServicoServico.objects.create(cliente=form.cleaned_data['cliente'],
                                                   servico=servico,
                                                   status=StatusPrestacaoServico.objects.get(descricao_curta="NAO_AGENDADO"),
                                                   discriminator='SERVICO',
                                                   recepcionista=UserProfile.objects.get(user=self.request.user).perfil_funcionario,
                                                   )
            messages.add_message(self.request, messages.SUCCESS, 'O servico %s foi adicionado.' % servico)

        #itera pelos pacotes de servico escolhidos
        for pacote in form.cleaned_data['pacote_servicos']:
            #1 adiciona o pacote do cliente
            psc = PacoteServicoCliente.objects.create(cliente=form.cleaned_data['cliente'],
                                                recepcionista=UserProfile.objects.get(user=self.request.user).perfil_funcionario,
                                                pacote_servico=pacote,
                                                )
            messages.add_message(self.request, messages.SUCCESS, 'O pacote %s foi adicionado.' % pacote)

            #2 adiciona cada servico do pacote comprado
            #  busca todos os servicos
            servico_pacote_servico_list = ServicoPacoteServico.objects.select_related('servico').filter(pacote_servico=pacote)
            for sps in servico_pacote_servico_list:
                #  cria cada servico contido no pacote como uma prestacao de servico nao agendada
                PrestacaoServicoPacote.objects.create(cliente=form.cleaned_data['cliente'],
                                                      pacoteServico_cliente=psc,
                                                      servico_pacoteservico=sps,
                                                      status=StatusPrestacaoServico.objects.get(descricao_curta="NAO_AGENDADO"),
                                                      discriminator='PACOTE',
                                                      recepcionista=UserProfile.objects.get(user=self.request.user).perfil_funcionario,
                                                      )
                messages.add_message(self.request, messages.SUCCESS, 'O servico %s do pacote %s foi adicionado.' % (sps.servico, pacote))

        form.cleaned_data['cliente'].atualiza_visto_em_agora()
        return HttpResponseRedirect(self.get_success_url()+"?cliente=%s&status__id__exact=1"%form.cleaned_data['cliente'].id)

