# -*- coding: UTF-8 -*-
from django import forms
from django.db import transaction
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
        servicos = forms.ModelMultipleChoiceField(queryset=Servico.objects.all() ,required=False, widget=forms.SelectMultiple(attrs={'style':"width: 200px; height: 280px"}))
        pacote_servicos = forms.ModelMultipleChoiceField(queryset=PacoteServico.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'style':"width: 200px; height: 280px"}))

    template_name = 'cadastro/cbv/prestacao_servico_novo.html'
    form_class = PrestacaoServicoNovoForm
    success_url = '/admin/cadastro/prestacaoservico'

    @transaction.commit_on_success
    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        from django.contrib import messages

        #itera pelos servicos escolhidos
        recepcionista = UserProfile.objects.get(user=self.request.user).perfil_funcionario
        for servico in form.cleaned_data['servicos']:
            #  cria cada servico contido na lista como uma prestacao de servico nao agendada para o cliente escolhido
            PrestacaoServico.novo_servico(cliente=form.cleaned_data['cliente'],servico=servico,recepcionista=recepcionista)
            messages.add_message(self.request, messages.SUCCESS, 'O servico %s foi adicionado.' % servico)

        #itera pelos pacotes de servico escolhidos
        for pacote in form.cleaned_data['pacote_servicos']:
            #1 adiciona o pacote do cliente
            PrestacaoServico.novo_pacote(cliente=form.cleaned_data['cliente'], pacote=pacote, recepcionista=recepcionista)
            messages.add_message(self.request, messages.SUCCESS, 'O pacote %s foi adicionado.' % pacote)

        form.cleaned_data['cliente'].atualiza_visto_em_agora()
        return HttpResponseRedirect(self.get_success_url()+"?cliente=%s&status__id__exact=1"%form.cleaned_data['cliente'].id)

