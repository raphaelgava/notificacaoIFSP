from datetime import datetime

from django.db import models
from django import forms
from django.forms import ModelForm

from .models import Aluno
from .models import Notificacao

class AlunoForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Senha')
    password_check = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Confirmar senha',)
    datanascimento = models.DateField("Data de nascimento", default=datetime.now())  # Field name made lowercase.

    class Meta:
        model = Aluno
        # fields = ('prontuario', 'first_name', 'last_name', 'email', 'password', 'senha2', 'sexo', 'datanascimento', 'turma',)
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_check', 'sexo', 'datanascimento', 'id_instituto', 'turma',)

    # def compare_password(self):
    #     user = self.model()
    #     user.set_password(password)
    #     if (senha2 = password)
    #         set_password(password)

    # def verify_password:


        # class NotificacaoForm(ModelForm):
#
#     class Meta:
#         model = Notificacao
#         fields = ('datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'prontuario', 'remetente',)