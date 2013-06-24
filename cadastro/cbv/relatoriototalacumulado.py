# -*- coding: UTF-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets
from cadastro.utils import safe_list_get


class Item:
    qtd_acum = 0
    custo_acum = 0
    valor_acum = 0
    diferenca_acum = 0
    qtd_share = 0
    custo_share = 0
    valor_share = 0
    diferenca_share = 0

class RelatorioTotalAcumulado(FormView):
    class BuscaForm(forms.Form):
        today = timezone.datetime.today() - relativedelta(months=1)
        primeiro_dia_mes = datetime.date(today.year, today.month, 1)
        ultimo_dia_mes = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        de = forms.DateField(widget=widgets.AdminDateWidget, required=False, initial=primeiro_dia_mes)
        ate = forms.DateField( widget=widgets.AdminDateWidget, required=False, initial=ultimo_dia_mes)

        servicos = forms.ModelMultipleChoiceField(queryset=Servico.objects.all() ,required=False, widget=forms.SelectMultiple(attrs={'style':"width: 100px; height: 100px"}))
        pacote_servicos = forms.ModelMultipleChoiceField(queryset=PacoteServico.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'style':"width: 100px; height: 100px"}))

        imprime_filtro = forms.BooleanField(initial=True, required=False)


    template_name = 'cadastro/cbv/relatoriototalacumuladofiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    @staticmethod
    def filtra_ate(ate, object_list):
        if ate is not None:
            object_list = object_list.filter(horario__data__lte=ate)
        return object_list

    @staticmethod
    def filtra_de(de, object_list):
        if de is not None:
            object_list = object_list.filter(horario__data__gte=de)
        return object_list

    def update(self, dict, key, custo, valor):
        dict[key] = safe_list_get(dict, key, Item())
        dict[key].qtd_acum += 1
        dict[key].custo_acum += custo
        dict[key].valor_acum += valor
        dict[key].diferenca_acum += (valor - custo)

    def atualiza_share(self, db, total):
        for item in db.values():
            item.qtd_share =   ( item.qtd_acum   / float(total.qtd_acum)   ) * 100 if total.qtd_acum   > 0 else 0
            item.custo_share = ( item.custo_acum / total.custo_acum ) * 100 if total.custo_acum > 0 else 0
            item.valor_share = ( item.valor_acum / total.valor_acum ) * 100 if total.valor_acum > 0 else 0
            item.diferenca_share = ( item.diferenca_acum / total.diferenca_acum ) * 100 if total.diferenca_acum > 0 else 0

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #acumuladores gerais
        db = {}
        db_espec = {}
        db_tipo = {}
        db_servico = {}
        db_pacote = {}

        #busca todos os servicos SIMPLES
        qs_pss = PrestacaoServicoServico.objects.filter(pagamento__isnull=False)
        if form.cleaned_data['servicos']:
            qs_pss = qs_pss.filter(servico__in=form.cleaned_data['servicos'])
        qs_pss = self.filtra_de(form.cleaned_data['de'], qs_pss)
        qs_pss = self.filtra_ate(form.cleaned_data['ate'], qs_pss)

        for pss in qs_pss:
            custo = pss.servico.custo_material
            valor = pss.servico.valor

            self.update(db_tipo, PrestacaoServico.SERVICO, custo, valor)
            self.update(db_servico, pss.servico, custo, valor)
            self.update(db_espec, pss.servico.especialidade, custo, valor)
            self.update(db, 'Geral', custo, valor)

        #busca todos os servicos de PACOTE
        qs_psp = PrestacaoServicoPacote.objects.filter(pacoteServico_cliente__pagamento__isnull=False)
        if form.cleaned_data['pacote_servicos']:
            qs_psp = qs_psp.filter(pacoteServico_cliente__pacote_servico__in=form.cleaned_data['pacote_servicos'])
        qs_psp = self.filtra_de(form.cleaned_data['de'], qs_psp)
        qs_psp = self.filtra_ate(form.cleaned_data['ate'], qs_psp)

        for psp in qs_psp:
            custo = psp.servico_pacoteservico.servico.custo_material
            valor = psp.servico_pacoteservico.valor_rateado
            
            self.update(db_tipo, PrestacaoServico.PACOTE, custo, valor)
            self.update(db_pacote, psp.servico_pacoteservico.servico, custo, valor)
            self.update(db_espec, psp.servico_pacoteservico.servico.especialidade, custo, valor)
            self.update(db, 'Geral', custo, valor)

        if len(qs_pss) >= 0 or len(qs_psp) >= 0:
            self.atualiza_share(db_tipo, db['Geral'])
            self.atualiza_share(db_espec, db['Geral'])
            self.atualiza_share(db_servico, db['Geral'])
            self.atualiza_share(db_pacote, db['Geral'])
            self.atualiza_share(db, db['Geral'])

        db_list = (("Visão Geral",db),
                   ("Visão por Tipo", db_tipo),
                   ("Visão por Especialidade",db_espec),
                   ("Visão por Serviços",db_servico),
                   ("Visão por Pacotes",db_pacote))

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatoriototalacumuladoresultado.html', {
            'form': form,
            'now': timezone.datetime.now(),
            'db_list': db_list,
            'object_count': db['Geral'].qtd_acum,
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))

