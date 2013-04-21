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

        self.e = Especialidade(descricao="manicure")
        self.e.save()


        self.s = Servico()
        self.s.nome = "corte teste"
        self.s.descricao = "corte teste"
        self.s.valor = 50
        self.s.comissao = 30
        self.s.custo_material = 2
        self.s.especialidade = self.e
        self.s.habilitado = True
        self.s.save()

        self.s2 = Servico()
        self.s2.nome = "servico2"
        self.s2.descricao = "servico2"
        self.s2.valor = 50
        self.s2.comissao = 30
        self.s2.custo_material = 2
        self.s2.especialidade = self.e
        self.s2.habilitado = True
        self.s2.save()

        self.ps = PacoteServico()
        self.ps.nome = "pacote teste"
        self.ps.descricao = "pacote teste"
        self.ps.valor = 80
        self.ps.habilitado = True
        self.ps.save()

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

    def test_servico(self):
        """
        test for Model.save()
        """
        e = Especialidade(descricao="manicure")
        e.save()

        s = Servico()
        s.nome = "corte teste"
        s.descricao = "corte teste"
        s.valor = 50
        s.comissao = 30
        s.custo_material = 2
        s.especialidade = e
        s.habilitado = True

        s.save()
        new = Servico.objects.get(id = s.id)
        self.assertTrue(s.nome == new.nome, "servico.save() don't working" )
        self.assertTrue(s.valor == new.valor, "servico.save() don't working" )
        self.assertTrue(s.especialidade == new.especialidade, "servico.save() don't working" )

    def test_pacoteservico(self):
        """
        test for Model.save()
        """
        ps = PacoteServico()
        ps.nome = "pacote teste"
        ps.descricao = "pacote teste"
        ps.valor = 80
        ps.habilitado = True
        ps.save()

        new = PacoteServico.objects.get(id = ps.id)
        self.assertTrue(ps.nome == new.nome, "pacoteservico.save() don't working" )
        self.assertTrue(ps.valor == new.valor, "pacoteservico.save() don't working" )

    def test_servicoPacoteServico(self):
        """
        test for Model.save()
        """
        sps = ServicoPacoteServico()
        sps.servico = self.s
        sps.pacote_servico = self.ps
        sps.valor_rateado = 40
        sps.save()

        new = ServicoPacoteServico.objects.get(id = sps.id)
        self.assertTrue(sps.servico == new.servico, "ServicoPacoteServico.save() don't working" )
        self.assertTrue(sps.pacote_servico == new.pacote_servico, "ServicoPacoteServico.save() don't working" )
        self.assertTrue(sps.valor_rateado == new.valor_rateado, "ServicoPacoteServico.save() don't working" )

        sps2 = ServicoPacoteServico()
        sps2.servico = self.s2
        sps2.pacote_servico = self.ps
        sps2.valor_rateado = 40
        sps2.save()

        new = ServicoPacoteServico.objects.get(id = sps2.id)
        self.assertTrue(sps2.servico == new.servico, "ServicoPacoteServico.save() don't working" )
        self.assertTrue(sps2.pacote_servico == new.pacote_servico, "ServicoPacoteServico.save() don't working" )
        self.assertTrue(sps2.valor_rateado == new.valor_rateado, "ServicoPacoteServico.save() don't working" )

        sps_list = ServicoPacoteServico.objects.filter(pacote_servico = self.ps)
        self.assertGreaterEqual(len(sps_list),2, "ServicoPacoteServico.save() don't working")
