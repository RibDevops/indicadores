from django import forms
from .models import (
    Status, TipoAcesso, TipoElo, Pais, Estado, RegiaoCidade,
    Comar, OM, Servidor, DataCompra, DataVisita,
)

_WIDGET_ATTRS = {'class': 'form-control'}
_SELECT_ATTRS = {'class': 'form-select'}


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


class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = ['sigla', 'nome', 'pais']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'pais': forms.Select(attrs=_SELECT_ATTRS),
        }


class RegiaoCidadeForm(forms.ModelForm):
    class Meta:
        model = RegiaoCidade
        fields = ['sigla', 'nome', 'estado']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'estado': forms.Select(attrs=_SELECT_ATTRS),
        }


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


class OMForm(forms.ModelForm):
    class Meta:
        model = OM
        fields = ['sigla', 'nome', 'comar', 'pais', 'tipo_elo', 'obs']
        widgets = {
            'sigla': forms.TextInput(attrs=_WIDGET_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'comar': forms.Select(attrs=_SELECT_ATTRS),
            'pais': forms.Select(attrs=_SELECT_ATTRS),
            'tipo_elo': forms.Select(attrs=_SELECT_ATTRS),
            'obs': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }


class ServidorForm(forms.ModelForm):
    class Meta:
        model = Servidor
        fields = [
            'om', 'status', 'tipo_acesso', 'nome',
            'data_aquisicao', 'sistema_operacional', 'versao_so', 'obs',
        ]
        widgets = {
            'om': forms.Select(attrs=_SELECT_ATTRS),
            'status': forms.Select(attrs=_SELECT_ATTRS),
            'tipo_acesso': forms.Select(attrs=_SELECT_ATTRS),
            'nome': forms.TextInput(attrs=_WIDGET_ATTRS),
            'data_aquisicao': forms.DateInput(attrs={**_WIDGET_ATTRS, 'type': 'date'}),
            'sistema_operacional': forms.TextInput(attrs=_WIDGET_ATTRS),
            'versao_so': forms.TextInput(attrs=_WIDGET_ATTRS),
            'obs': forms.Textarea(attrs={**_WIDGET_ATTRS, 'rows': 3}),
        }


class DataCompraForm(forms.ModelForm):
    class Meta:
        model = DataCompra
        fields = ['servidor', 'data_compra']
        widgets = {
            'servidor': forms.Select(attrs=_SELECT_ATTRS),
            'data_compra': forms.DateInput(attrs={**_WIDGET_ATTRS, 'type': 'date'}),
        }


class DataVisitaForm(forms.ModelForm):
    class Meta:
        model = DataVisita
        fields = ['servidor', 'data_visita']
        widgets = {
            'servidor': forms.Select(attrs=_SELECT_ATTRS),
            'data_visita': forms.DateInput(attrs={**_WIDGET_ATTRS, 'type': 'date'}),
        }
