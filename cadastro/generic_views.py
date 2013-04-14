# -*- coding: utf-8 -*-
from django.http import HttpResponse

from django.core import serializers
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from utils import filter_model_from_querystring, get_model_or_404, model_to_modelform
from django.shortcuts import redirect

@csrf_exempt
def generic_get_json(request, model_name, app_name, relations={}, extras=('id',), indent=4, excludes=(), return_type='json', instance_id=None):
    """
    Retorna o json do APP_NAME.MODEL_NAME informados.
    http://baby.bilouro.com/<app_name>/<model_name>/list.json

    EXEMPLOS:
    http://baby.bilouro.com/agenda/presenca/list/.json?aluno__turma__id=1
    http://baby.bilouro.com/agenda/aluno/list/.json?turma=1
    http://baby.bilouro.com/agenda/classificacao/list/.json?tipo=10
    http://baby.bilouro.com/agenda/notificacao/list/.json?dia_hora__gte=2012-01-01&dia_hora__lte=2012-01-01

    FILTROS:
    Pode-se utilizar filtros via querystring como aluno__id=1 e/ou resumo_icontains='etad'
    filtros adicionais: (BASTA SEGUIR O PADRAO DJANGO OBJECTS.FILTER())

    UTILIZACAO MAIS SIMPLES:
    Onde o model_name é buscado diretamente da url, automagicamente todos os modelos estão extensíveis via json
    (r'^(?P<model_name>\w+)/list[/]{0,1}.json$', 'util.generic_views.generic_get_json' ),
    *pode ser colocado no URLS.PY RAIZ, desta forma informando a APP_NAME via url*
    (r'^(?P<app_name>\w+)/(?P<model_name>\w+)/list[/]{0,1}.json$', 'util.generic_views.generic_get_json' ),

    PERSONALIZANDO O JSON:
    Para personalizar, passe parametros adicionais no urls.py.
    EX:
    (r'^atividade/list[/]{0,1}.json$', 'util.generic_views.generic_get_json', {
        'model_name':'atividade',
        'relations':('turma',)
    }),

    """
    serializer = serializers.get_serializer(return_type)()
    model = get_model_or_404(app_name, model_name)

    if instance_id:
        list = model.objects.filter(id=instance_id)
    else:
        list = model.objects.all()
        list = filter_model_from_querystring(list, request)

    response = HttpResponse()
    serializer.serialize(
        list,
        stream=response,
        relations=relations,
        extras=extras,
        excludes=excludes,
        indent=indent
    )

    return response


def generic_add_edit(request, model_name, app_name, instance_id=None):
    """
    salva ou edita um APP_NAME.MODEL_NAME atraves da
    classe ModelForm.

    as validações ficam a cargo das validações nativas de cada entidade/fieldtype
    """
    DATA = request.POST or request.GET
    model = get_model_or_404(app_name, model_name)
    ModelForm = model_to_modelform(model)
    if instance_id:
        form = ModelForm(DATA, instance=get_object_or_404(model, id=instance_id))
    else:
        form = ModelForm(DATA)

    if form.is_valid():
        try:
            o = form.save()
            return redirect( o.get_absolute_url('json') )
        except:
            return HttpResponse('2')
    else:
        return HttpResponse('1')

def generic_delete(request, model_name, app_name, instance_id):
    """
    deleta um APP_NAME.MODEL_NAME atraves do id
    """
    model = get_model_or_404(app_name, model_name)
    object_tobe_deleted = get_object_or_404(model, id=instance_id)
    try:
        object_tobe_deleted.delete()
        return HttpResponse('0')
    except:
        return HttpResponse('2')
