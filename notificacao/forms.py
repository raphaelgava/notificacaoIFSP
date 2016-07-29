from datetime import datetime

from django import forms
from django.db import models
from django.forms import ModelForm

from .models import Aluno
from .models import Pessoa
from .models import Servidor


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# class AlunoForm(ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Senha')
#     password_check = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Confirmar senha',)
#     datanascimento = models.DateField("Data de nascimento", default=datetime.now())  # Field name made lowercase.
#
#     class Meta:
#         model = Aluno
#         fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_check', 'sexo', 'datanascimento', 'id_instituto', 'turma',)

class _PersonForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Senha')
    password_check = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Confirmar senha', )
    datanascimento = models.DateField("Data de nascimento", default=datetime.now())  # Field name made lowercase.

    class Meta:
        model = Pessoa
        abstract = True
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password', 'password_check', 'sexo', 'datanascimento',
            'id_instituto',)


class AlunoForm(_PersonForm):
    class Meta:
        model = Aluno
        fields = _PersonForm.Meta.fields + ('turma',)


class ServidorForm(_PersonForm):
    class Meta:
        model = Servidor
        fields = _PersonForm.Meta.fields + ('funcao',)


        # class NotificacaoForm(ModelForm):
        #
        #     class Meta:
        #         model = Notificacao
        #         fields = ('datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'prontuario', 'remetente',)
