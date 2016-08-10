from datetime import datetime

from django import forms
from django.db import models
from django.forms import ModelForm

from .models import Aluno
from .models import Pessoa
from .models import Professor
from .models import Servidor


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    # def clean_remember_me(self):
    #     """clean method for remember_me """
    #     remember_me = self.cleaned_data.get['remember_me']
    #     if not remember_me:
    #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    #     else:
    #         settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
    #     return remember_me


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

        # def clean(self):
        #     password = self.cleaned_data.get('password')
        #     password_check = self.cleaned_data.get('password_check')
        #
        #     if password != password_check:
        #         raise forms.ValidationError("Passwords don't match")
        #
        #     return self.cleaned_data


class AlunoForm(_PersonForm):
    class Meta:
        model = Aluno
        fields = _PersonForm.Meta.fields + ('turma',)


class ServidorForm(_PersonForm):
    class Meta:
        model = Servidor
        fields = _PersonForm.Meta.fields + ('funcao',)


class ProfessorForm(ServidorForm):
    class Meta:
        model = Professor
        fields = ServidorForm.Meta.fields + ('formacao', 'id_tipo')
