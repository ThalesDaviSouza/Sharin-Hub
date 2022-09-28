from django import forms
from django.forms import ModelForm
from .models import Publicacao

class PublicaForm(ModelForm):
    class Meta:
        model = Publicacao
        fields = ('titulo', 'descricao', 'telefone', 'tags')

        labels = {
            'titulo': '',
            'descricao': '',
            'telefone': '',
            'tags': '',
        }

        widgets = {
            'titulo':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Título'
                }),
            'descricao':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Descrição'
                }),
            'telefone':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Telefone'
                }),
            'tags':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Tags'
                }),
        }