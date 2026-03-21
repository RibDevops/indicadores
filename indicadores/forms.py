from django import forms
from django.utils import timezone

from .models import (
    Status, TipoAcesso, TipoElo, Pais, Estado, RegiaoCidade,
    Comar, OM, Servidor, DataVisita,
)

_WIDGET_ATTRS = {'class': 'form-control'}
_SELECT_ATTRS = {'class': 'form-select'}


def _reject_future_date(value, field_label='Data'):
    """Raise ValidationError if *value* is in the future."""
    if value and value > timezone.now().date():
        raise forms.ValidationError(
            f'{field_label} não pode ser uma data futura.'
        )
    return value


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['descricao']
        widgets = {'descricao': forms.TextInput(attrs=_WIDGET_ATTRS)}


class TipoAcessoForm(forms.ModelForm):
    class Meta:
        model = TipoAcesso
        fields = ['tipo']
        widgets = {'tipo': forms.TextInput(attrs=_WIDGET_ATTRS)}


class TipoEloForm(forms.ModelForm):
    class Meta:
        model = TipoElo
        fields = ['tipo', 'descricao']
        widgets = {
            'tipo': forms.TextInput(attrs=_WIDGET_ATTRS),
            'descricao': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }


class PaisForm(forms.ModelForm):
    class Meta:
        model = Pais
        fields = ['sigla', 'nome']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
        }

    def clean_sigla(self):
        return self.cleaned_data['sigla'].upper()


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['sigla', 'nome', 'pais']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'pais': forms.Select(attrs=_SELECT_ATTRS),
        }

    def clean_sigla(self):
        return self.cleaned_data['sigla'].upper()


class RegiaoCidadeForm(forms.ModelForm):
    class Meta:
        model = RegiaoCidade
        fields = ['sigla', 'nome', 'estado']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'estado': forms.Select(attrs=_SELECT_ATTRS),
        }

    def clean_sigla(self):
        return self.cleaned_data['sigla'].upper()


class ComarForm(forms.ModelForm):
    class Meta:
        model = Comar
        fields = ['sigla', 'nome', 'regiao_cidade', 'obs']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'regiao_cidade': forms.Select(attrs=_SELECT_ATTRS),
            'obs': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }

    def clean_sigla(self):
        return self.cleaned_data['sigla'].upper()


class OMForm(forms.ModelForm):
    class Meta:
        model = OM
        # servidor é opcional — pode ser vinculado depois
        fields = ['servidor', 'sigla', 'nome', 'comar', 'pais', 'tipo_elo', 'obs']
        widgets = {
            # Servidor aparece como select; campo em branco = sem vínculo
            'servidor': forms.Select(attrs=_SELECT_ATTRS),
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'comar': forms.Select(attrs=_SELECT_ATTRS),
            'pais': forms.Select(attrs=_SELECT_ATTRS),
            'tipo_elo': forms.Select(attrs=_SELECT_ATTRS),
            'obs': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }

    def clean_sigla(self):
        return self.cleaned_data['sigla'].upper()


class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        # om foi removido daqui — a FK agora fica em OM.servidor
        fields = [
            'status', 'tipo_acesso', 'nome',
            'data_aquisicao', 'sistema_operacional', 'versao_so', 'suporte_so', 'obs',
        ]
        widgets = {
            'status': forms.Select(attrs=_SELECT_ATTRS),
            'tipo_acesso': forms.Select(attrs=_SELECT_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            # format='%Y-%m-%d' garante que o valor seja pré-preenchido corretamente
            # no input type="date" ao editar (o HTML espera o formato YYYY-MM-DD)
            'data_aquisicao': forms.DateInput(attrs={**_WIDGET_ATTRS, 'type': 'date'}, format='%Y-%m-%d'),
            'sistema_operacional': forms.TextInput(attrs=_WIDGET_ATTRS),
            'versao_so': forms.TextInput(attrs=_WIDGET_ATTRS),
            'suporte_so': forms.Select(attrs=_SELECT_ATTRS),
            'obs': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }

    def clean_data_aquisicao(self):
        return _reject_future_date(
            self.cleaned_data.get('data_aquisicao'), 'Data de aquisição'
        )


class DataVisitaForm(forms.ModelForm):
    class Meta:
        model = DataVisita
        fields = ['servidor', 'data_visita']
        widgets = {
            'servidor': forms.Select(attrs=_SELECT_ATTRS),
            # format='%Y-%m-%d' garante que o valor seja pré-preenchido corretamente
            # no input type="date" ao editar (o HTML espera o formato YYYY-MM-DD)
            'data_visita': forms.DateInput(attrs={**_WIDGET_ATTRS, 'type': 'date'}, format='%Y-%m-%d'),
        }

    def clean_data_visita(self):
        return _reject_future_date(
            self.cleaned_data.get('data_visita'), 'Data de visita'
        )
