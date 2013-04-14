# -*- coding: utf-8 -*-
import math
import re

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