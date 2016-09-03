# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange model' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the model, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime

from colorfield.fields import ColorField
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from polymodels.models import PolymorphicModel


# todo: verificar o pq do unresolved reference (ESTA FUNCIONANDO!!!)

# todo: tipo formacao ainda falta cadastrar


class Remetente(PolymorphicModel):
    descricao = models.CharField("Descrição", max_length=50)  # Field name made lowercase.
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = 'Remetente'
        verbose_name_plural = 'Remetentes'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def activeAgain(self, *args, **kwargs):
        self.is_active = True
        self.save()

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


class Instituto(Remetente):
    datafundacao = models.DateField("Data de fundação", help_text=_('dd/mm/yyyy'), blank=True,
                                    null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Instituto'
        verbose_name_plural = 'Institutos'


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Prontuário'),
        max_length=8,
        unique=True,
        help_text=_('Required. 7 characters.'),
        validators=[
            validators.RegexValidator(
                r'^[\w]+$',
                _('Enter a valid username. This value may contain only '
                  'letters, numbers ' 'characters.')
            ),
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'))
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # abstract = True

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def activeAgain(self, *args, **kwargs):
        self.is_active = True
        self.save()

class Pessoa(Usuario):
    SEXO = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    )
    sexo = models.CharField(max_length=10, default='Masculino',
                            choices=SEXO)  # Field name made lowercase.
    datanascimento = models.DateField("Data de nascimento", help_text=_('dd/mm/yyyy'),
                                      default=timezone.now)  # Field name made lowercase.
    id_instituto = models.ForeignKey(Instituto, blank=True, null=True)  # Field name made lowercase.

    class Meta(Usuario.Meta):
        abstract = True
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{} {}'.format(self.username, self.first_name)


# todo: procurar ppc do curso para tirar os dados
# todo: definir mascara para os campos de data!
class Servidor(Pessoa):
    funcao = models.CharField("Função", max_length=30)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'


class Professor(Servidor):
    formacao = models.CharField("Área", max_length=20)  # Field name made lowercase.
    id_tipo = models.ForeignKey('Tipoformacao', verbose_name="Tipo formação", blank=True,
                                null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class Aluno(Pessoa):
    turma = models.CharField(max_length=10)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Disciplina(models.Model):
    descricao = models.CharField("Descrição", max_length=50)  # Field name made lowercase.
    is_active = models.BooleanField(_('active'), default=True)

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    def activeAgain(self, *args, **kwargs):
        self.is_active = True
        self.save()

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)

class Curso(Remetente):
    id_instituto = models.ForeignKey(Instituto)  # Field name made lowercase.
    disciplinas = models.ManyToManyField(Disciplina)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Local(models.Model):
    # latitude = models.IntegerField()  # Field name made lowercase.
    # longitude = models.IntegerField()  # Field name made lowercase.
    position = GeopositionField()
    descricao = models.CharField("Descrição", max_length=30)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


class TipoNotificacao(models.Model):
    descricao = models.CharField("Título", max_length=20)  # Field name made lowercase.
    cor = ColorField()

    class Meta:
        verbose_name = 'Tipo Notificação'
        verbose_name_plural = 'Tipos Notificações'

    # essa definição é para mostrar o título na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


#todo: verificar se será necessário colocar dia e hora de termino assim como o is_active
class Notificacao(models.Model):
    datahora = models.DateTimeField("Data notificação", auto_now_add=True)  # Field name made lowercase.
    id_tipo = models.ForeignKey(TipoNotificacao, verbose_name="Tipo notificação")  # Field name made lowercase.
    id_local = models.ForeignKey(Local, verbose_name="Local", blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField("Descrição", max_length=255)  # Field name made lowercase.
    titulo = models.CharField("Título", max_length=45)  # Field name made lowercase.
    servidor = models.ForeignKey(Servidor)  # Field name made lowercase.
    remetente = models.ManyToManyField(Remetente)

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    # essa definição é para mostrar o título na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.titulo)


class Oferecimento(Remetente):
    SEMESTER = (
        (1, 'Primeiro'),
        (2, 'Segundo'),
    )

    YEAR_CHOICES = []
    for r in range(datetime.datetime.now().year, (datetime.datetime.now().year + 5)):
        YEAR_CHOICES.append((r, r))

    ano = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semestre = models.IntegerField(default=1, choices=SEMESTER)  # Field name made lowercase.
    id_professor = models.ForeignKey(Professor)  # Field name made lowercase.
    id_disciplina = models.ForeignKey(Disciplina)  # Field name made lowercase.
    alunos = models.ManyToManyField(Aluno)

    class Meta:
        verbose_name = 'Oferecimento'
        verbose_name_plural = 'Oferecimentos'


class SalaAlunos(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    alunos = models.ManyToManyField(Aluno)

    class Meta:
        verbose_name = 'Sala Alunos'
        verbose_name_plural = 'Salas Alunos'


class SalaProfessores(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    professores = models.ManyToManyField(Professor)

    class Meta:
        verbose_name = 'Sala Professores'
        verbose_name_plural = 'Salas Professores'


class TipoFormacao(models.Model):
    descricao = models.CharField("Descrição", max_length=30)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Tipo Formação'
        verbose_name_plural = 'Tipos Formações'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)
