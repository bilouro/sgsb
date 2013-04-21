from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from cadastro.models import *
#from cadastro.models import Cliente, Funcionario, UserProfile


class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento', 'data_cadastro', 'status')
    date_hierarchy = 'data_cadastro'
    search_fields = ['nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    list_filter = ['status',]

class PessoaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class DependenteFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('funcionario', 'nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento')
    date_hierarchy = 'data_nascimento'
    search_fields = ['nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'funcionario__nome'] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    list_filter = ['funcionario',]

class DependenteFuncionarioInline(admin.TabularInline):
    model = DependenteFuncionario
    fk_name = 'funcionario'
    exclude = ('endereco', 'telefone', 'email',)
    extra = 0
class EspecialidadeFuncionarioInline(admin.TabularInline):
    model = EspecialidadeFuncionario
    extra = 1
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor', 'data_nascimento', 'data_admissao', 'status', 'cargo')
    date_hierarchy = 'data_admissao'
    search_fields = ['nome', 'endereco', 'telefone', 'email', 'cpf', 'identidade', 'orgao_expedidor' ] #,'turma__nome', 'palavras_chave']
    #ordering = ('-dia',)
    inlines = [ DependenteFuncionarioInline, EspecialidadeFuncionarioInline]
    list_filter = ['status','cargo']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','perfil_cliente', 'perfil_funcionario')
    #date_hierarchy = 'dia'
    search_fields = ['user__username','user__first_name', 'user__last_name', 'perfil_cliente__nome', 'perfil_funcionario__nome' ]
    #ordering = ('-dia',)
    #list_filter = ['turma','periodo']

class StatusClienteAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class StatusFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('descricao','habilitado',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    list_filter = ['habilitado',]

class CargoAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class EspecialidadeAdmin(admin.ModelAdmin):
    list_display = ('descricao',)
    #date_hierarchy = 'data_admissao'
    search_fields = ['descricao',]
    #ordering = ('-dia',)
    #list_filter = ['status',]

class EspecialidadeFuncionarioAdmin(admin.ModelAdmin):
    list_display = ('especialidade','funcionario')
    #date_hierarchy = 'data_admissao'
    search_fields = ['especialidade__descricao','funcionario__descricao']
    #ordering = ('-dia',)
    list_filter = ['especialidade','funcionario']

admin.site.register(StatusCliente, StatusClienteAdmin)
admin.site.register(StatusFuncionario, StatusFuncionarioAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(DependenteFuncionario, DependenteFuncionarioAdmin)
admin.site.register(EspecialidadeFuncionario,EspecialidadeFuncionarioAdmin )
admin.site.register(Especialidade, EspecialidadeAdmin)

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Pessoa, PessoaAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(UserProfile, UserProfileAdmin)

#modelos uteis do django
admin.site.register(Session)
admin.site.register(Permission)
admin.site.register(ContentType)

