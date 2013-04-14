from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from cadastro.models import *
#from cadastro.models import Cliente, Funcionario, UserProfile


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    #date_hierarchy = 'dia'
    search_fields = ['nome', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    #date_hierarchy = 'dia'
    search_fields = ['nome', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    #date_hierarchy = 'dia'
    search_fields = ['nome', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','perfil_cliente', 'perfil_funcionario')
    #date_hierarchy = 'dia'
    search_fields = ['user__username','user__first_name', 'user__last_name', 'perfil_cliente__nome', 'perfil_funcionario__nome' ]
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

#modelos uteis do django
admin.site.register(Session)
admin.site.register(Permission)
admin.site.register(ContentType)

