from datetime import datetime

from colorfield.fields import ColorField
from django import forms
from django.db import models
from django.forms import ModelForm

from .models import Aluno
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Pessoa
from .models import Professor
from .models import Remetente
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao


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


# ==========================================CADASTRO USUARIOS===========================================================
# todo: criar máscara para o campo de prontuário
class _PersonForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Senha')
    password_check = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Confirmar senha')
    datanascimento = models.DateField("Data de nascimento", default=datetime.now())  # Field name made lowercase.

    class Meta:
        model = Pessoa
        abstract = True
        fields = (
            'username', 'first_name', 'last_name', 'email', 'password', 'password_check', 'sexo', 'datanascimento',
            'id_instituto',)


# todo: tornar obrigatório selecionar um instituto!!!!

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
        fields = _PersonForm.Meta.fields + ('formacao', 'id_tipo',)


# ======================================================================================================================

# ==========================================CADASTRO REMETENTE==========================================================

class _RemetenteForm(ModelForm):
    class Meta:
        model = Remetente
        abstract = True
        fields = ('descricao',)


class InstitutoForm(_RemetenteForm):
    datafundacao = models.DateField("Data de fundação", default=datetime.now())  # Field name made lowercase.

    class Meta:
        model = Instituto
        fields = _RemetenteForm.Meta.fields + ('datafundacao',)


class OferecimentoForm(_RemetenteForm):
    id_professor = forms.ModelChoiceField(queryset=Professor.objects.filter(is_active=True))
    id_disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.filter(is_active=True))
    alunos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Aluno.objects.filter(is_active=True))
    class Meta:
        model = Oferecimento
        fields = _RemetenteForm.Meta.fields + ('ano', 'semestre', 'id_professor', 'id_disciplina', 'alunos')


# ======================================================================================================================



# ==========================================CADASTRO OUTROS=============================================================
# todo: mudar remetente (mesmo esquema do alunos)
class NotificacaoForm(ModelForm):
    descricao = forms.CharField(widget=forms.Textarea(
        attrs={
            'id': 'my_description',
            'onkeyup':
            # 'mostrarResultado(this.value,255,"spcontando");'
                'contarCaracteres(this.value,255,"sprestante");',
        }),
        max_length=255, )

    class Meta:
        model = Notificacao
        fields = ('id_tipo', 'id_local', 'remetente', 'titulo', 'descricao',)

class DisciplinaForm(ModelForm):
    class Meta:
        model = Disciplina
        fields = ('descricao',)


class LocalForm(ModelForm):
    class Meta:
        model = Local
        fields = ('position', 'descricao',)

class TipoNotificacaoForm(ModelForm):
    cor = ColorField("Data de fundação", default='#FFFFFF')  # Field name made lowercase.

    class Meta:
        model = TipoNotificacao
        fields = ('descricao', 'cor',)


class TipoFormacaoForm(ModelForm):
    class Meta:
        model = TipoFormacao
        fields = ('descricao',)

# ======================================================================================================================
