import datetime

from django.test import TestCase
from django.utils import timezone

from .forms import (
    DataCompraForm, DataVisitaForm, ServidorForm,
    PaisForm, EstadoForm, RegiaoCidadeForm, ComarForm, OMForm,
)
from .models import (
    Pais, Estado, RegiaoCidade, Comar, OM,
    Status, TipoAcesso, TipoElo, Servidor,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_fixtures():
    """Create the minimum set of related objects needed by ServidorForm tests."""
    pais = Pais.objects.create(sigla='BR', nome='Brasil')
    estado = Estado.objects.create(sigla='RJ', nome='Rio de Janeiro', pais=pais)
    regiao = RegiaoCidade.objects.create(sigla='RJ-CAP', nome='Rio de Janeiro', estado=estado)
    comar = Comar.objects.create(sigla='COMAR1', nome='I COMAR', regiao_cidade=regiao)
    tipo_elo = TipoElo.objects.create(tipo='Fibra')
    om = OM.objects.create(sigla='OM1', nome='Organização Militar 1', comar=comar, pais=pais, tipo_elo=tipo_elo)
    status = Status.objects.create(descricao='Ativo')
    tipo_acesso = TipoAcesso.objects.create(tipo='SSH')
    return om, status, tipo_acesso


def _servidor_data(om, status, tipo_acesso, data_aquisicao):
    return {
        'om': om.pk,
        'status': status.pk,
        'tipo_acesso': tipo_acesso.pk,
        'nome': 'SRV-TEST',
        'data_aquisicao': data_aquisicao,
        'sistema_operacional': 'Linux',
        'versao_so': 'Ubuntu 22.04',
        'suporte_so': 'atual',
    }


# ---------------------------------------------------------------------------
# Date validation
# ---------------------------------------------------------------------------

class ServidorFormDateValidationTest(TestCase):

    def setUp(self):
        self.om, self.status, self.tipo_acesso = _make_fixtures()

    def test_past_date_is_valid(self):
        past = timezone.now().date() - datetime.timedelta(days=365)
        form = ServidorForm(data=_servidor_data(self.om, self.status, self.tipo_acesso, past))
        self.assertTrue(form.is_valid(), form.errors)

    def test_today_is_valid(self):
        today = timezone.now().date()
        form = ServidorForm(data=_servidor_data(self.om, self.status, self.tipo_acesso, today))
        self.assertTrue(form.is_valid(), form.errors)

    def test_future_date_is_invalid(self):
        future = timezone.now().date() + datetime.timedelta(days=1)
        form = ServidorForm(data=_servidor_data(self.om, self.status, self.tipo_acesso, future))
        self.assertFalse(form.is_valid())
        self.assertIn('data_aquisicao', form.errors)

    def test_future_date_error_message(self):
        future = timezone.now().date() + datetime.timedelta(days=30)
        form = ServidorForm(data=_servidor_data(self.om, self.status, self.tipo_acesso, future))
        form.is_valid()
        self.assertIn('não pode ser uma data futura', form.errors['data_aquisicao'][0])


class DataCompraFormDateValidationTest(TestCase):

    def setUp(self):
        om, status, tipo_acesso = _make_fixtures()
        self.servidor = Servidor.objects.create(
            om=om, status=status, tipo_acesso=tipo_acesso,
            nome='SRV-DC', data_aquisicao=datetime.date(2020, 1, 1),
            sistema_operacional='Linux', versao_so='Debian 11',
        )

    def test_past_compra_is_valid(self):
        past = timezone.now().date() - datetime.timedelta(days=10)
        form = DataCompraForm(data={'servidor': self.servidor.pk, 'data_compra': past})
        self.assertTrue(form.is_valid(), form.errors)

    def test_future_compra_is_invalid(self):
        future = timezone.now().date() + datetime.timedelta(days=1)
        form = DataCompraForm(data={'servidor': self.servidor.pk, 'data_compra': future})
        self.assertFalse(form.is_valid())
        self.assertIn('data_compra', form.errors)


class DataVisitaFormDateValidationTest(TestCase):

    def setUp(self):
        om, status, tipo_acesso = _make_fixtures()
        self.servidor = Servidor.objects.create(
            om=om, status=status, tipo_acesso=tipo_acesso,
            nome='SRV-DV', data_aquisicao=datetime.date(2020, 1, 1),
            sistema_operacional='Linux', versao_so='Debian 11',
        )

    def test_past_visita_is_valid(self):
        past = timezone.now().date() - datetime.timedelta(days=5)
        form = DataVisitaForm(data={'servidor': self.servidor.pk, 'data_visita': past})
        self.assertTrue(form.is_valid(), form.errors)

    def test_future_visita_is_invalid(self):
        future = timezone.now().date() + datetime.timedelta(days=7)
        form = DataVisitaForm(data={'servidor': self.servidor.pk, 'data_visita': future})
        self.assertFalse(form.is_valid())
        self.assertIn('data_visita', form.errors)


# ---------------------------------------------------------------------------
# Sigla normalization (uppercase)
# ---------------------------------------------------------------------------

class SiglaNormalizationTest(TestCase):

    def test_pais_sigla_uppercased(self):
        form = PaisForm(data={'sigla': 'br', 'nome': 'Brasil'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'BR')

    def test_pais_sigla_mixed_case_uppercased(self):
        form = PaisForm(data={'sigla': 'Br', 'nome': 'Brasil'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'BR')

    def test_pais_sigla_already_upper_unchanged(self):
        form = PaisForm(data={'sigla': 'BR', 'nome': 'Brasil'})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'BR')

    def test_estado_sigla_uppercased(self):
        pais = Pais.objects.create(sigla='BR', nome='Brasil')
        form = EstadoForm(data={'sigla': 'rj', 'nome': 'Rio de Janeiro', 'pais': pais.pk})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'RJ')

    def test_regiao_cidade_sigla_uppercased(self):
        pais = Pais.objects.create(sigla='BR', nome='Brasil')
        estado = Estado.objects.create(sigla='RJ', nome='Rio de Janeiro', pais=pais)
        form = RegiaoCidadeForm(data={'sigla': 'rj-cap', 'nome': 'Capital', 'estado': estado.pk})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'RJ-CAP')

    def test_comar_sigla_uppercased(self):
        pais = Pais.objects.create(sigla='BR', nome='Brasil')
        estado = Estado.objects.create(sigla='RJ', nome='Rio de Janeiro', pais=pais)
        regiao = RegiaoCidade.objects.create(sigla='RJ-CAP', nome='Capital', estado=estado)
        form = ComarForm(data={'sigla': 'comar1', 'nome': 'I COMAR', 'regiao_cidade': regiao.pk})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'COMAR1')

    def test_om_sigla_uppercased(self):
        pais = Pais.objects.create(sigla='BR', nome='Brasil')
        estado = Estado.objects.create(sigla='RJ', nome='Rio de Janeiro', pais=pais)
        regiao = RegiaoCidade.objects.create(sigla='RJ-CAP', nome='Capital', estado=estado)
        comar = Comar.objects.create(sigla='COMAR1', nome='I COMAR', regiao_cidade=regiao)
        tipo_elo = TipoElo.objects.create(tipo='Fibra')
        form = OMForm(data={
            'sigla': 'om1', 'nome': 'OM Teste',
            'comar': comar.pk, 'pais': pais.pk, 'tipo_elo': tipo_elo.pk,
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data['sigla'], 'OM1')
