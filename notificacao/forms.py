from colorfield.fields import ColorField
from django import forms
from django.forms import ModelForm
from django.forms.widgets import TextInput

from .models import Aluno
from .models import Curso
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Pessoa
from .models import Professor
from .models import Remetente
from .models import SalaAlunos
from .models import SalaProfessores
from .models import Servidor
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
class _PersonForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Senha')
    password_check = forms.CharField(widget=forms.PasswordInput(), max_length=10, label='Confirmar senha')
    username = forms.CharField(disabled=True)
    datanascimento = forms.CharField(label='Data de nascimento')  # forms.DateInput.input_type = "date"
    # datanascimento = models.DateField("Data de nascimento", default=datetime.now())  # Field name made lowercase.

    def __init__(self, *args, **kwargs):
        super(_PersonForm, self).__init__(*args, **kwargs)
        self.fields['datanascimento'].widget = TextInput(attrs={
            'class': 'datas',
            'placeholder': 'Data de nascimento'
        })

    # username = forms.CharField(widget=forms.TextInput(
    #     attrs={
    #         'id': 'username',
    #         #'placeholder': 'XXXXXX-X',
    #         #'onkeypress': 'mascara(this, "######-#");',
    #         'placeholder': 'XXXXXXX',
    #         'onkeypress': 'mascara(this, "#######");',
    #     }),
    #     max_length=7, )

    class Meta:
        model = Pessoa
        abstract = True
        fields = (
            'username',
            'first_name', 'last_name', 'email', 'password', 'password_check', 'sexo', 'datanascimento',
            'id_instituto',)


class AlunoForm(_PersonForm):
    class Meta:
        model = Aluno
        fields = _PersonForm.Meta.fields + ('turma',)


class ServidorForm(_PersonForm):
    class Meta:
        model = Servidor
        fields = _PersonForm.Meta.fields + ('funcao','admin',)


class ProfessorForm(ServidorForm):
    class Meta:
        model = Professor
        fields = _PersonForm.Meta.fields + ('formacao', 'tipo_formacao', 'admin',)


# ======================================================================================================================

# ==========================================CADASTRO REMETENTE==========================================================

class _RemetenteForm(ModelForm):
    class Meta:
        model = Remetente
        abstract = True
        fields = ('descricao', 'is_active')


# class DateInput(forms.DateInput):
#     input_type = 'date'

class InstitutoForm(_RemetenteForm):
    datafundacao = forms.DateInput.input_type = "date"

    # datafundacao = models.DateField("Data de fundação", default=datetime.now())  # Field name made lowercase.

    class Meta:
        model = Instituto
        fields = _RemetenteForm.Meta.fields + ('datafundacao',)
        # widgets = {
        #     'datafundacao': DateInput(),
        # }


class OferecimentoForm(_RemetenteForm):
    id_professor = forms.ModelChoiceField(queryset=Professor.objects.filter(is_active=True))
    id_disciplina = forms.ModelChoiceField(queryset=Disciplina.objects.filter(is_active=True))
    alunos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Aluno.objects.filter(is_active=True), required=False)
    dataInicio = forms.CharField(label='Data Início')  # forms.DateInput.input_type = "date"

    def __init__(self, *args, **kwargs):
        super(OferecimentoForm, self).__init__(*args, **kwargs)
        self.fields['dataInicio'].widget = TextInput(attrs={
            'class': 'datas',
            'placeholder': 'Data Início'
        })

    class Meta:
        model = Oferecimento
        fields = _RemetenteForm.Meta.fields + (
        'ano', 'semestre', 'week', 'time', 'dataInicio', 'qtd', 'id_professor', 'id_disciplina', 'alunos')
        # 'ano', 'semestre', 'week', 'time', 'period', 'dataInicio', 'qtd', 'id_professor', 'id_disciplina', 'alunos')


class CursoForm(_RemetenteForm):
    id_instituto = forms.ModelChoiceField(queryset=Instituto.objects.filter(is_active=True))
    # disciplinas = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
    #                                              queryset=Disciplina.objects.filter(is_active=True))

    class Meta:
        model = Curso
        fields = _RemetenteForm.Meta.fields + ('id_instituto', 'sigla', 'qtd_modulos', 'carga_horaria')


class SalaAlunosForm(_RemetenteForm):
    id_curso = forms.ModelChoiceField(queryset=Curso.objects.filter(is_active=True))
    alunos = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                            queryset=Aluno.objects.filter(is_active=True))

    class Meta:
        model = SalaAlunos
        fields = _RemetenteForm.Meta.fields + ('id_curso', 'alunos')



class SalaProfessoresForm(_RemetenteForm):
    id_curso = forms.ModelChoiceField(queryset=Curso.objects.filter(is_active=True))
    professores = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                                 queryset=Professor.objects.filter(is_active=True))

    class Meta:
        model = SalaProfessores
        fields = _RemetenteForm.Meta.fields + ('id_curso', 'professores')


# ======================================================================================================================



# ==========================================CADASTRO OUTROS=============================================================
class NotificacaoForm(ModelForm):
    descricao = forms.CharField(widget=forms.Textarea(
        attrs={
            'id': 'my_description',
            'onkeyup':
            # 'mostrarResultado(this.value,255,"spcontando");'
                'contarCaracteres(this.value,255,"sprestante");',
        }),
        max_length=255, )

    remetente = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                               queryset=Remetente.objects.filter(is_active=True))

    class Meta:
        model = Notificacao
        fields = ('id_tipo', 'id_local', 'remetente', 'titulo', 'descricao',)


class DisciplinaForm(ModelForm):
    id_curso = forms.ModelChoiceField(queryset=Curso.objects.filter(is_active=True))
    class Meta:
        model = Disciplina
        fields = ('descricao', 'id_curso', 'is_active'
                  #           'sigla',
                  #            'id_curso'
                  )


class LocalForm(ModelForm):
    class Meta:
        model = Local
        fields = ('position', 'descricao',)

class TipoNotificacaoForm(ModelForm):
    cor = ColorField("Data de fundação", default='#FFFFFF')  # Field name made lowercase.

    class Meta:
        model = TipoNotificacao
        fields = ('descricao', 'cor',)

# ======================================================================================================================
