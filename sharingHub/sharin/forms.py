from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from .models import Publicacao

class PublicaForm(ModelForm):
    class Meta:
        model = Publicacao
        fields = ('titulo', 'descricao', 'telefone', 'tags')

        labels = {
            'titulo': 'Título',
            'descricao': 'Descrição',
            'telefone': 'Telefone',
            'tags': 'Tags',
        }

        widgets = {
            'titulo':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Título'
                }),
            'descricao':forms.Textarea(attrs = {
                'class':'form-control',
                'placeholder':'Descrição'
                }),
            'telefone':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Telefone: (31) 9 9999-9999'
                }),
            'tags':forms.TextInput(attrs = {
                'class':'form-control',
                'placeholder':'Tags'
                }),
        }


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

    