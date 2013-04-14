"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from cadastro.models import Cliente, Funcionario, UserProfile
from django.contrib.contenttypes.models import ContentType
from unidecode import unidecode

from django.test import TestCase


class DataBaseTest(TestCase):

    def setUp(self):
        super(DataBaseTest, self).setUp()

        self.hoje = datetime.date.today()
        self.c = Cliente(nome="test")
        self.c.save()

        self.f = Funcionario(nome="test")
        self.f.save()

        self.u = User()
        self.u.username = "bilouro"
        self.u.save()

    def test_Cliente(self):
        """
        test for Model.save()
        """
        initial_list_count = len(Cliente.objects.all())
        c = Cliente(nome="test")
        c.save()
        new = Cliente.objects.get(id = c.id)
        self.assertTrue(c.nome == new.nome, "Client.save() don't working" )

    def test_Funcionario(self):
        """
        test for Model.save()
        """
        initial_list_count = len(Funcionario.objects.all())
        f = Funcionario(nome="test")
        f.save()
        new = Funcionario.objects.get(id = f.id)
        self.assertTrue(f.nome == new.nome, "Funcionario.save() don't working" )

    def test_UserProfile(self):
        """
        test for Model.save()
        """
        initial_list_count = len(UserProfile.objects.all())
        up = UserProfile(perfil_funcionario = self.f, perfil_cliente = self.c, user=self.u)
        up.save()
        new = UserProfile.objects.get(id = up.id)
        self.assertTrue(up.perfil_cliente== new.perfil_cliente, "UserProfile.save() don't working" )
        self.assertTrue(up.perfil_funcionario == new.perfil_funcionario, "UserProfile.save() don't working" )
        self.assertTrue(up.user == new.user, "UserProfile.save() don't working" )
