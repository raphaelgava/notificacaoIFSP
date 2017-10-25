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
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core import validators
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from geoposition.fields import GeopositionField
from polymodels.models import PolymorphicModel
from rest_framework.authtoken.models import Token


# http://cheng.logdown.com/posts/2015/10/27/how-to-use-django-rest-frameworks-token-based-authentication
# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# def token_request(request):
#     if user_requested_token() and token_request_is_warranted():
#         new_token = Token.objects.create(user=request.user)


# todo: mudar a classe ObtainAuthToken em authtokenn\view para fazer a retirada da criptografia!!!



class Remetente(PolymorphicModel):
    descricao = models.CharField("Descrição", max_length=50)  # Field name made lowercase.
    tipo = models.CharField("Tipo", max_length=50, default="Tipo")
    is_active = models.BooleanField(_('active'), default=True)

    # tipo_remetente = models.CharField("Tipo Remetente", max_length=20)

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
        return '{} - {}'.format(self.tipo, self.descricao)


class Instituto(Remetente):
    datafundacao = models.DateField("Data Fundação", default=timezone.now)

    # datafundacao = models.DateField("Data de fundação", help_text=_('dd/mm/yyyy'), blank=True, null=True)  # Field name made lowercase.
    # objects = Remetente()

    class Meta:
        verbose_name = 'Instituto'
        verbose_name_plural = 'Institutos'


# todo: fazer o esqueci a senha e enviar por email!!!
# todo: criar a opção de alterar os meus dados!
class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        _('Prontuário'),
        max_length=7,
        unique=True,
        help_text=_('Required. 7 characters.'),
        validators=[
            validators.RegexValidator(
                #r'^([0-9]{6}-?[0-9]{1})(?!\w|\.)$', #999999-9
                r'([0-9]{7})(?!\w|\.)$',#9999999
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

    def checkGroup(self, *args, **kwargs):
        return self.groups.first()

    def isProfessor(self, *args, **kwargs):
        prof = Professor.objects.filter(pk=self.pk)
        if prof is not None:
            if len(prof) > 0:
                return True

        return False

class Pessoa(Usuario):
    SEXO = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    )
    sexo = models.CharField(max_length=10, default='Masculino', choices=SEXO)  # Field name made lowercase.
    datanascimento = models.DateField("Data de nascimento", default=timezone.now)
    # datanascimento = models.DateField("Data de nascimento", help_text=_('dd/mm/yyyy'),
    #                                  default=timezone.now)  # Field name made lowercase.

    #   null=True sets NULL (versus NOT NULL) on the column in your DB. Blank values for Django field types such as
    #   DateTimeField or ForeignKey will be stored as NULL in the DB.
    #
    #   blank=True determines whether the field will be required in forms. This includes the admin and your own custom
    #   forms. If blank=True then the field will not be required, whereas if it's False the field cannot be blank.
    id_instituto = models.ForeignKey(Instituto, blank=False, null=True)  # Field name made lowercase.
    cpf = models.CharField(max_length=11, blank=False, null=False, default='00000000000')

    class Meta(Usuario.Meta):
        abstract = True
        # verbose_name = 'Pessoa'
        # verbose_name_plural = 'Pessoas'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{} - {} {} {}'.format(self.username, self.cpf, self.first_name, self.last_name)
        # return '{} - {} {}'.format(self.username, self.first_name, self.last_name)

class Servidor(Pessoa):
    funcao = models.CharField("Função", max_length=30)  # Field name made lowercase.
    admin = models.BooleanField("Admin sistema", default=False)

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'


class Professor(Servidor):
    TIPO_FORMACAO = (
        ('Técnico', 'Técnico'),
        ('Graduação', 'Graduação'),
        ('Pós Graduação', 'Pós Graduação'),
        ('Mestrado', 'Mestrado'),
        ('Doutorado', 'Doutorado'),
        ('Pós Doutorado', 'Pós Doutorado'),
        ('Livre Docência', 'Livre Docência'),
    )
    formacao = models.CharField("Área", max_length=20)  # Field name made lowercase.
    tipo_formacao = models.CharField(verbose_name="Tipo formação", default='Graduação', max_length=15,
                                     choices=TIPO_FORMACAO)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

class Curso(Remetente):
    id_instituto = models.ForeignKey(Instituto)  # Field name made lowercase.
    sigla = models.CharField("Sigla", max_length=4, blank=False)
    qtd_modulos = models.IntegerField("Módulos", blank=False, default=8)
    carga_horaria = models.IntegerField("Carga horária", blank=False, default=3200)

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Turma(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    # alunos = models.ManyToManyField(Aluno, blank=True, null=True)
    sigla = models.CharField(max_length=10)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turma'


class Aluno(Pessoa):
    turma = models.CharField(max_length=10)  # Field name made lowercase.
    pkTurma = models.ForeignKey(Turma, verbose_name="Turma")  # Field name made lowercase.

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

    def __str__(self):
        # turma = Turma.objects.get(pk=self.pkTurma)
        return '{} - {} {} {} - {}'.format(self.username, self.cpf, self.first_name, self.last_name, self.turma)


class Disciplina(models.Model):
    descricao = models.CharField("Descrição", max_length=50)  # Field name made lowercase.
    sigla = models.CharField("Sigla", max_length=4, blank=False, default='DDD')  # Field name made lowercase.
    id_curso = models.ForeignKey(Curso, verbose_name="Curso")
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


# todo: verificar se o tempo da notificaçao esta em 24h
# todo: esse dia e hora é o fim da notificação o dia do evento!!!
class Notificacao(models.Model):
    # datahora = models.DateTimeField("Data notificação", auto_now_add=True)  # Field name made lowercase.
    datahora = models.DateField("Data Acontecimento", default=timezone.now)
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
    YEAR_CHOICES = []
    for r in range(datetime.datetime.now().year, (datetime.datetime.now().year + 5)):
        YEAR_CHOICES.append((r, r))


    SEMESTER = (
        (1, 'Primeiro'),
        (2, 'Segundo'),
    )

    WEEK = (
        (1, 'Segunda'),
        (2, 'Terça'),
        (3, 'Quarta'),
        (4, 'Quinta'),
        (5, 'Sexta'),
    )

    TIME = (
        (1, 'Primeiro'),
        (2, 'Segundo'),
        (3, 'Terceiro'),
        (4, 'Quarto'),
        (5, 'Quinto'),
    )

    QTD = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    # PERIOD = (
    #     (1, 'Matutino'),
    #     (2, 'Vespertino'),
    #     (3, 'Noturno'),
    # )

    ano = models.IntegerField(_('year'), choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semestre = models.IntegerField(default=1, choices=SEMESTER)  # Field name made lowercase.
    week = models.IntegerField("Dia da semana", default=1, choices=WEEK)  # Field name made lowercase.
    time = models.IntegerField("Horário", default=1, choices=TIME)  # Field name made lowercase.
    # period = models.IntegerField("Período", default=1, choices=PERIOD)  # Field name made lowercase.
    qtd = models.IntegerField("Quantidade de aulas", default=2, choices=QTD)
    id_professor = models.ForeignKey(Professor, blank=True, null=True)  # Field name made lowercase.
    professor = models.CharField("Professor", max_length=61, default="Professor teste")
    sigla = models.CharField("Sigla", max_length=4, blank=False, default='DDD')  # Field name made lowercase.
    id_disciplina = models.ForeignKey(Disciplina)  # Field name made lowercase.
    # alunos = models.ManyToManyField(Aluno, blank=True, null=True, through='OferecimentoAlunos')
    alunos = models.ManyToManyField(Aluno, blank=True, null=True)
    id_curso = models.IntegerField("Curso", default=0)
    # dataInicio = models.DateField("Data Início", help_text=_('dd/mm/yyyy'), default=timezone.now)
    dataInicio = models.DateField("Data Início", default=timezone.now)

    class Meta:
        verbose_name = 'Oferecimento'
        verbose_name_plural = 'Oferecimentos'


# class OferecimentoAlunos(models.Model):
#     id_aluno = models.ForeignKey(Aluno, blank=True, null=True)  # Field name made lowercase.
#     id_oferecimento = models.ForeignKey(Oferecimento, blank=True, null=True)  # Field name made lowercase.
#
#     class Meta:
#         auto_created = True
#         verbose_name = 'Oferecimento Alunos'
#         verbose_name_plural = 'Oferecimento Alunos'

class SalaProfessores(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    professores = models.ManyToManyField(Professor)

    class Meta:
        verbose_name = 'Sala Professores'
        verbose_name_plural = 'Salas Professores'
