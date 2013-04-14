# -*- coding: utf-8 -*-
import math
import re
from django import forms
import datetime
from django.core.exceptions import MultipleObjectsReturned
import logging

logger = logging.getLogger(__name__)

def get_querystring_as_dict_from_url(url):
    """
    Retorna um dicionario com os parametros(key) recebidos por querystring e seus valores(value)
    """
    from urlparse import urlparse
    url = urlparse(url)
    return dict( [x.split('=') for x in url[4].split('&')] )


def get_querystring_as_dict_from_request(request):
    """
    Retorna um dicionario com os parametros(key) recebidos por querystring e seus valores(value)
    """
    kwargs = {}
    for k,v in request.GET.items():
        kwargs[str(k)] = str(v)

    return kwargs

def filter_model_from_querystring(query_set, request):
    """
    Se tiver algum parametro queryString
    eh usado como filter para o model
    #ex: ?prototipo__pk=24&localizacao__pk=396
    """
    kwargs = get_querystring_as_dict_from_request(request)
    if kwargs:
        query_set = query_set.filter(**kwargs)

    return query_set

def se_nulo_valor(texto, valor):
    if texto:
        return texto
    else:
        return valor

def datetime_to_text_safe(data_hora, retorna_now_se_nulo=False, date_hora_se_nulo=None, str_retorno_se_nulo=""):
    try:
        return data_hora.strftime('%d/%m/%y %H:%Mh')
    except:
        if retorna_now_se_nulo:
            return datetime_to_text_safe(datetime.datetime.now())
        elif date_hora_se_nulo:
            return datetime_to_text_safe(date_hora_se_nulo)
        else:
            return str_retorno_se_nulo

def rad(number):
    return number * math.pi / 180
    

def calc_distance_between_points(point1_lat, point1_lng, point2_lat, point2_lng):
      r = 6371 #earth's mean radius in km
      dLat  = rad(point2_lat - point1_lat)
      dLong = rad(point2_lng - point1_lng)
    
      a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(rad(point1_lat)) * math.cos(rad(point2_lat)) * math.sin(dLong/2) * math.sin(dLong/2)
      c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
      d = r * c
    
      return round(d, 2)
  
_translate = lambda cpf: ''.join(re.findall("\d", cpf))

def _gen(cpf):
    """Gera o pr√≥ximo d√≠gito do n√∫mero de CPF

    """
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0

class CPF(object):
    _gen = staticmethod(_gen)
    _translate = staticmethod(_translate)
    
    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:
        12345678910
        123.456.789-10
        ou uma lista ou tuple
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0)
        """
        
        if isinstance(cpf, basestring):
            if not cpf.isdigit():
               cpf = self._translate(cpf)
               cpf = cpf.replace(".", "" )
               cpf = cpf.replace("-", "" )
               cpf = cpf.replace(" ", "" )
            
        self.cpf = [int(x) for x in cpf]

    def __getitem__(self, index):
        """Retorna o d√≠gito em index como string

        """
        
        return self.cpf[index]

    def __repr__(self):
        """Retorna uma representa√ß√£o 'real', ou seja:

        eval(repr(cpf)) == cpf
        
        """
        
        return "CPF('%s')" % ''.join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """Prov√™ teste de igualdade para n√∫meros de CPF

        """

        return isinstance(other, CPF) and self.cpf == other.cpf
    
    def __str__(self):
        """Retorna uma representa√ß√£o do CPF na forma:

        123.456.789-10

        """

        d = iter("..-")
        s = map(str, self.cpf)
        for i in xrange(3, 12, 4):
            s.insert(i, d.next())
        r = ''.join(s)
        return r

    def isValid(self):
        """Valida o n√∫mero de cpf

        """
        
        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]
    
def decode_text(texto):
    senha_decoded = ''
    for letra in texto:
        senha_decoded += chr(ord(letra)-1)
    return senha_decoded


def get_model_or_404(app_name, model_name):
    """
    retorna um modelo de acordo com o APP_NAME.MODEL_NAME informados
    Lanca: http404 se não achar
    """
    from django.db.models.loading import get_model
    from django.http import Http404
    model_name = get_model(app_name, model_name)
    if model_name is None:
        raise Http404
    return model_name

def model_to_modelform(model):
    """
    Cria e Retorna a Classe ModelForm associada ao model passado.
    """
    meta = type('Meta', (), { "model":model, })
    modelform_class = type('modelform', (forms.ModelForm,), {"Meta": meta})
    return modelform_class

def generic_get_absolute_url(self, return_type=None):
    """
    Cria o absolute url de acordo com model.app_label + model.name + model.id
    ex:
    /agenda/notificacao/1
    com json:
    /agenda/notificacao/1.json
    com xml:
    /agenda/notificacao/1.xml
    """
    return_type_url = ''
    if return_type and return_type in ('json', 'xml'):
        return_type_url = '.%s' % return_type

    return "/%s/%s/%s%s" % (self._meta.app_label, self.__class__.__name__.lower(), self.id, return_type_url)

def safe_list_get(list, index, default=None):
    """
    busca na lista/dict de forma segura.
    retorna default se não achar o item da lista/dict
    """
    try:
        return list[index]
    except (IndexError, KeyError):
        return default

def get_object_safe_or_default(model_object, retorna_objeto_default=True, **kwargs):
    """
    Inverso do get_object_or_404.
    Retorna o objeto de acordo com o filtro e se nao
      for achado chama get_default do model_object e retorna.

    Não levanta exception, mas retorna None nos seguintes casos:
      * Se não encontrar retorna None (vide obs)
      * Se encotrar mais que um retorna None

    obs: se retorna_objeto_default=True entao retorna um objeto mockado
    """
    try:
        return model_object.objects.get(**kwargs)
    except model_object.DoesNotExist:
        return model_object.get_default(**kwargs) if retorna_objeto_default else None
    except MultipleObjectsReturned:
        logger.error( 'Mais de um objeto foi retornado em: %s' % repr(**kwargs))
        return None

def get_object_list_or_default(model_object, retorna_objeto_default=True, **kwargs):
    """
    Similar ao get_object_safe_or_default
    Retorna uma lista de acordo com o filtro e se nao
      for achado chama get_default do model_object e retorna uma lista com um elemento
    """
    object_list = model_object.objects.filter(**kwargs)
    if len(object_list) == 0 and retorna_objeto_default:
        return [ model_object.get_default(**kwargs) ]

    return object_list

def get_all_object_or_default(model_object, retorna_objeto_default=True, **kwargs):
    """
    Retorna todos os objetos de um modelo se nao achar nenhum
      chama get_default do model_object e retorna uma lista com um elemento
    """
    object_list = model_object.objects.all()
    if len(object_list) == 0:
        return [model_object.get_default(**kwargs)] if retorna_objeto_default else []
    else:
        return object_list

def get_first_object_or_default(model_object, retorna_objeto_default=True, **kwargs):
    """
    Retorna um o primeiro objeto da lista e se nao houver nenhum
      chama get_default do model_object e o retorna
    """
    list = get_all_object_or_default( model_object, retorna_objeto_default, **kwargs)
    # o parametro retorna_objeto_default eh verificado e adequadamente aplicado na funcao get_all_object_or_default
    if len(list) > 0:
        return list[0]
    else:
        return None