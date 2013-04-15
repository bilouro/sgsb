"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from cadastro.models import *
from django.contrib.contenttypes.models import ContentType
from unidecode import unidecode

from django.test import TestCase

class DataBaseTest(TestCase):

    def setUp(self):
        super(DataBaseTest, self).setUp()


        self.hoje = timezone.datetime.today()
        self.agora = timezone.now()

        self.status_cliente = StatusCliente(descricao="ativo")
        self.status_cliente.save()

        self.c = Cliente(nome="test", data_cadastro=self.agora, status=self.status_cliente)
        self.c.save()

        self.status_funcionario = StatusFuncionario(descricao="ativo")
        self.status_funcionario.save()

        self.cargo = Cargo(descricao="funcionario")
        self.cargo.save()

        self.f = Funcionario(nome="test", data_admissao=self.hoje, status = self.status_funcionario, cargo=self.cargo)
        self.f.save()

        self.u = User()
        self.u.username = "test_user"
        self.u.save()

    def test_Cliente(self):
        """
        test for Model.save()
        """
        c = Cliente(nome="test", data_cadastro=self.agora, status=self.status_cliente)
        c.save()
        new = Cliente.objects.get(id = c.id)
        self.assertTrue(c.nome == new.nome, "Client.save() don't working" )

    def test_Funcionario(self):
        """
        test for Model.save()
        """
        f = Funcionario(nome="test", data_admissao=self.hoje, status = self.status_funcionario, cargo=self.cargo)
        f.save()
        new = Funcionario.objects.get(id = f.id)
        self.assertTrue(f.nome == new.nome, "Funcionario.save() don't working" )

    def test_DependenteFuncionario(self):
        """
        test for Model.save()
        """
        f = Funcionario(nome="test", data_admissao=self.hoje, status = self.status_funcionario, cargo=self.cargo)
        f.save()
        df = DependenteFuncionario(nome="test", funcionario=f)
        df.save()
        new = DependenteFuncionario.objects.get(id = df.id)
        self.assertTrue(f.nome == new.nome, "DependenteFuncionario.save() don't working" )

    def test_EspecialidadeFuncionario(self):
        """
        test for Model.save()
        """
        e = Especialidade(descricao="manicure")
        e.save()
        f = Funcionario(nome="test", data_admissao=self.hoje, status = self.status_funcionario, cargo=self.cargo)
        f.save()
        ef = EspecialidadeFuncionario(funcionario = f, especialidade = e)
        ef.save()

        new = EspecialidadeFuncionario.objects.get(id = ef.id)
        self.assertTrue(ef.funcionario == new.funcionario, "EspecialidadeFuncionario.save() don't working" )
        self.assertTrue(ef.especialidade == new.especialidade, "EspecialidadeFuncionario.save() don't working" )

    def test_UserProfile(self):
        """
        test for Model.save()
        """
        up = UserProfile(perfil_funcionario = self.f, perfil_cliente = self.c, user=self.u)
        up.save()
        new = UserProfile.objects.get(id = up.id)
        self.assertTrue(up.perfil_cliente== new.perfil_cliente, "UserProfile.save() don't working" )
        self.assertTrue(up.perfil_funcionario == new.perfil_funcionario, "UserProfile.save() don't working" )
        self.assertTrue(up.user == new.user, "UserProfile.save() don't working" )