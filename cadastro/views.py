# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required

#from django import forms
#from django.core import serializers
#from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, Http404
#from django.core.urlresolvers import reverse
#from django.template import RequestContext
#from django.core.paginator import Paginator
#from django.contrib.auth import logout
#from django.core.files.base import ContentFile
#from django.db.models import Q

#from django.contrib.auth.models import User
#from django.db import transaction

#from django.utils import simplejson
#from django.core.cache import cache

#import datetime
from django.conf import settings
from util import utils
from django.views.generic.list import ListView
from django.utils import timezone

from cadastro.models import *

@login_required
def index(request):
    return render_to_response('index.html', {'user':request.user})


@login_required
def cria_agenda(request):
    import calendar, datetime,itertools

    ANO=2013
    MES=5


    #todos ids que tem ao menos uma especialidade
    id_funcionario_com_especialidade_list = EspecialidadeFuncionario.objects.all().values_list('funcionario__id', flat=True).distinct()



    #busca os funcionarios
    funcionario_com_especialidade_list = \
        Funcionario.objects.filter( id__in = id_funcionario_com_especialidade_list )

    primeiro_dia_mes = datetime.date(ANO,MES,1)
    ult_dia_mes=calendar.monthrange(ANO,MES)[1]
    de_zero_a_ult_dia_mes_list = range(ult_dia_mes)
    #busca os horarios disponiveis
    horario_disponivel_list = HorarioDisponivel.objects.all()

    hdf_list = []
    for horario, funcionario, dias_a_somar in \
        itertools.product(
            horario_disponivel_list,
            funcionario_com_especialidade_list,
            de_zero_a_ult_dia_mes_list):

       hdf = HorarioDisponivelFuncionario()
       hdf.data = primeiro_dia_mes + \
                  datetime.timedelta(days=dias_a_somar)
       hdf.hora = horario
       hdf.funcionario = funcionario
       hdf.disponivel = True
       hdf_list.append(hdf)

    # cria todas de uma só vez
    HorarioDisponivelFuncionario.objects.bulk_create(hdf_list)

class PrestacaoServicoListView(ListView):

    model = PrestacaoServico

    def get_context_data(self, **kwargs):
        context = super(PrestacaoServicoListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context