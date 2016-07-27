# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

# class Pessoa(models.Model):
#     SEXO = (
#         ('Masculino', 'Masculino'),
#         ('Feminino', 'Feminino'),
#     )
#     prontuario = models.IntegerField("Prontuário",unique=True)  # Field name made lowercase.
#     nome = models.CharField(max_length=50)  # Field name made lowercase.
#     senha = models.CharField(max_length=10)  # Field name made lowercase.
#     sexo = models.CharField(max_length=10, default='Masculino', blank=False, null=False, choices=SEXO)  # Field name made lowercase.
#     datanascimento = models.DateField("Data de nascimento")  # Field name made lowercase.
#     email = models.EmailField(max_length=50, blank=True, null=True)  # Field name made lowercase.
#     ativo = models.BooleanField(default=True)  # Field name made lowercase. This field type is a guess.
#     id_instituto = models.ForeignKey('Instituto')  # Field name made lowercase.
#
#     class Meta:
#         abstract=True
#         verbose_name = 'Pessoa'
#         verbose_name_plural = 'Pessoas'
#
#     # essa definição é para mostrar a descrição na lista dos cadastros
#     def __str__(self):
#         return '{} - {}'.format(self.prontuario, self.nome)


class Pessoa(AbstractUser):
    SEXO = (
        ('Masculino', 'Masculino'),
        ('Feminino', 'Feminino'),
    )
    sexo = models.CharField(max_length=10, default='Masculino', blank=False, null=False, choices=SEXO)  # Field name made lowercase.
    datanascimento = models.DateField("Data de nascimento", default=timezone.now)  # Field name made lowercase.
    id_instituto = models.ForeignKey('Instituto', blank=True, null=True)  # Field name made lowercase.

    # USERNAME_FIELD = 'username'

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        # abstract=True
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{} - {}'.format(self.username, self.first_name)

class Servidor(Pessoa):
    funcao = models.CharField("Função", max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'


class Professor(Servidor):
    formacao = models.CharField("Área", max_length=20, blank=True, null=True)  # Field name made lowercase.
    id_tipo = models.ForeignKey('Tipoformacao', verbose_name="Tipo formação")  # Field name made lowercase.

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class Aluno(Pessoa):
    turma = models.CharField(max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Remetente(models.Model):
    descricao = models.CharField("Descrição", max_length=50)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Remetente'
        verbose_name_plural = 'Remetentes'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)

class Curso(Remetente):
    id_instituto = models.ForeignKey('Instituto')  # Field name made lowercase.
    ativo = models.BooleanField(default=True)  # Field name made lowercase. This field type is a guess.
    disciplinas = models.ManyToManyField('Disciplina')
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Disciplina(models.Model):
    descricao = models.CharField("Descrição", max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Disciplina'
        verbose_name_plural = 'Disciplinas'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


class Local(models.Model):
    latitude = models.IntegerField()  # Field name made lowercase.
    longitude = models.IntegerField()  # Field name made lowercase.
    descricao = models.CharField("Descrição", max_length=30)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'

    # essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


class Notificacao(models.Model):
    datahora = models.DateTimeField("Data notificação", primary_key=True, auto_now_add=True)  # Field name made lowercase.
    id_tipo = models.ForeignKey('Tiponotificacao', verbose_name="Tipo notificação")  # Field name made lowercase.
    id_local = models.ForeignKey(Local, verbose_name="Local", blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField("Descrição", max_length=255)  # Field name made lowercase.
    titulo = models.CharField("Título", max_length=45)  # Field name made lowercase.
    # prontuario = models.ForeignKey('Servidor', null=False, blank=False)  # Field name made lowercase.
    username = models.ForeignKey('Servidor', null=False, blank=False)  # Field name made lowercase.
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

    ano = models.DateField(default=datetime.date.today)  # Field name made lowercase.
    semestre = models.IntegerField(default=1, choices=SEMESTER)  # Field name made lowercase.
    id_professor = models.ForeignKey(Professor)  # Field name made lowercase.
    id_disciplina = models.ForeignKey(Disciplina)  # Field name made lowercase.
    alunos = models.ManyToManyField(Aluno)

    class Meta:
        verbose_name = 'Oferecimento'
        verbose_name_plural = 'Oferecimentos'


class Instituto(Remetente):
    datafundacao = models.DateField("Data de fundação", blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Instituto'
        verbose_name_plural = 'Institutos'


class Salaalunos(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    alunos = models.ManyToManyField(Aluno)

    class Meta:
        verbose_name = 'Sala Alunos'
        verbose_name_plural = 'Salas Alunos'


class Salaprofessores(Remetente):
    id_curso = models.ForeignKey(Curso, blank=True, null=True)  # Field name made lowercase.
    professores = models.ManyToManyField(Professor)

    class Meta:
        verbose_name = 'Sala Professores'
        verbose_name_plural = 'Salas Professores'


class Tipoformacao(models.Model):
    descricao = models.CharField("Descrição", max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Tipo Formação'
        verbose_name_plural = 'Tipos Formações'

    #essa definição é para mostrar a descrição na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.descricao)


class Tiponotificacao(models.Model):
    titulo = models.CharField("Título", max_length=20, blank=True, null=True)  # Field name made lowercase.
    cor = models.CharField(max_length=7, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        verbose_name = 'Tipo Notificação'
        verbose_name_plural = 'Tipos Notificações'

    # essa definição é para mostrar o título na lista dos cadastros
    def __str__(self):
        return '{}'.format(self.titulo)