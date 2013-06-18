# -*- coding: UTF-8 -*-
from django import forms
from django.db.models.query_utils import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import timezone
from django.views.generic.edit import FormView
from cadastro.models import *

from django.contrib.admin import widgets

class RelatorioPacotePendente(FormView):
    class BuscaForm(forms.Form):
        TIPO_RELATORIO=[
                ('10-','Pagos e não realizados'),
                ('01-','Não pagos e realizados'),
                ('001','Não pagos e não realizados'),
        ]
        cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False)
        pacotes = forms.ModelMultipleChoiceField(queryset=PacoteServico.objects.all(), required=False)

        tipo_relatorio = forms.ChoiceField(choices=TIPO_RELATORIO, widget=forms.RadioSelect(), initial='10-')
        imprime_filtro = forms.BooleanField(initial=True, required=False)

    template_name = 'cadastro/cbv/relatoriopacotependentefiltro.html'
    form_class = BuscaForm
    #success_url = '/cadastro/relatorio/funcionario/resultado'

    def form_valid(self, form):
        """
        Metodo chamado apos o form ser corretamente validado.
        O form ja se valida automaticamente de acordo com a declaracao de cada um.
        ex: DateField exige uma data valida.. o mesmo para os outros...
        """
        #busca todos os funcionarios
        object_list = PacoteServicoCliente.objects.all()

        if form.cleaned_data['cliente']:
            #se prencheu admissao_de entao busta todas as admissoes maiores(greater than) ou iguais(equal) a data digitada(gte)
            object_list = object_list.filter(cliente=form.cleaned_data['cliente'])

        if form.cleaned_data['pacotes']:
            #se prencheu admissao_de entao busta todas as admissoes menores(less than) ou iguais(equal) a data digitada(lte)
            object_list = object_list.filter(pacote_servico__in=form.cleaned_data['pacotes'])

        if form.cleaned_data['tipo_relatorio']:
            #busca apenas pacotes pagos ou nao pagos
            pago = form.cleaned_data['tipo_relatorio'][0]=='1'
            #os pacotes pagos tem pagamento__isnull=False
            pago_isnull = not pago
            object_list = object_list.filter(pagamento__isnull=pago_isnull)

            tipo_relatorio = {}
            #busca aqueles que tem pelo menos um servico *NAO* realizado
            tipo_relatorio['0'] = [ StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.AGENDADO),
                                   StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.NAO_AGENDADO) ]

            #busca aqueles que tem pelo menos um servico realizado
            tipo_relatorio['1'] = [ StatusPrestacaoServico.getStatusPrestacaoServicoInstance(StatusPrestacaoServico.REALIZADO), ]

            psc_id_list = PrestacaoServicoPacote.objects.filter(
                    status__in = tipo_relatorio[form.cleaned_data['tipo_relatorio'][1]]
                ).values_list('pacoteServico_cliente__id', flat=True).distinct()
            object_list = object_list.filter(id__in=psc_id_list)

            excecao = {}
            excecao['-']=None
            excecao['0']=None
            excecao['1']=tipo_relatorio['1']
            if excecao[ form.cleaned_data['tipo_relatorio'][2] ]:
                psc_id_list = PrestacaoServicoPacote.objects.filter(
                        status__in = excecao[ form.cleaned_data['tipo_relatorio'][2] ]
                    ).values_list('pacoteServico_cliente__id', flat=True).distinct()
                object_list = object_list.exclude(id__in=psc_id_list)

        #chama o template resultado enviando o form, a lista_final,
        # a data atual e a informacao se imprime ou nao o form
        return render_to_response('cadastro/cbv/relatoriopacotependenteresultado.html', {
            'form': form,
            'object_list':object_list.order_by('cliente'),
            'now': timezone.datetime.now(),
            'imprime_filtro': form.cleaned_data['imprime_filtro']
        }, context_instance=RequestContext(self.request))
