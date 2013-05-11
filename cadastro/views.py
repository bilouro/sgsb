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

#from prototipoIphone.prototipo.models import *
#from prototipoIphone.prototipo.forms import *

#from django.utils import simplejson
#from django.core.cache import cache

#import datetime
#import re
from django.conf import settings
from util import utils
from cadastro.models import *

@login_required
def index(request):
    return render_to_response('index.html', {'user':request.user})


@login_required
def cria_agenda(request):
    import calendar, datetime

    ANO=2013
    MES=5

    ult_dia_mes=calendar.monthrange(ANO,MES)[1]
    d = datetime.date(ANO,MES,1)
    dias_list = range(ult_dia_mes)

    #todos ids que tem ao menos uma especialidade
    id_funcionario_com_especialidade_list = EspecialidadeFuncionario.objects.all().values_list('funcionario__id', flat=True).distinct()
    #busca os funcionarios
    funcionario_com_especialidade_list = Funcionario.objects.filter(id__in= id_funcionario_com_especialidade_list)

    #busca os horarios disponiveis
    horario_disponivel_list = HorarioDisponivel.objects.all()

    for h,f,soma in itertools.product(horario_disponivel_list, funcionario_com_especialidade_list, dias_list):
       hdf = HorarioDisponivelFuncionario()
       hdf.data = d + datetime.timedelta(days=soma)
       hdf.hora = h
       hdf.funcionario = f
       hdf.disponivel = True
       hdf.save()
