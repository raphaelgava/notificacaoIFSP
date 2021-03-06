# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-10-09 02:37
from __future__ import unicode_literals

import colorfield.fields
import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import geoposition.fields
from django.conf import settings
from django.db import migrations, models

def apply_migration(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.bulk_create([
        Group(name=u'Student'),
        Group(name=u'Employee'),
        Group(name=u'Professor'),
        Group(name=u'Admin'),
    ])

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'},
                                              help_text='Required. 7 characters.', max_length=7, unique=True,
                                              validators=[
                                                  django.core.validators.RegexValidator('([0-9]{7})(?!\\w|\\.)$',
                                                                                        'Enter a valid username. This value may contain only letters, numbers characters.')],
                                              verbose_name='Prontuário')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Disciplina',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('sigla', models.CharField(default='DDD', max_length=4, verbose_name='Sigla')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplinas',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('descricao', models.CharField(max_length=30, verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Local',
                'verbose_name_plural': 'Locais',
            },
        ),
        migrations.CreateModel(
            name='Notificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datahora', models.DateTimeField(auto_now_add=True, verbose_name='Data notificação')),
                ('descricao', models.CharField(max_length=255, verbose_name='Descrição')),
                ('titulo', models.CharField(max_length=45, verbose_name='Título')),
                ('id_local', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notificacao.Local', verbose_name='Local')),
            ],
            options={
                'verbose_name': 'Notificação',
                'verbose_name_plural': 'Notificações',
            },
        ),
        migrations.CreateModel(
            name='Remetente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=50, verbose_name='Descrição')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Remetente',
                'verbose_name_plural': 'Remetentes',
            },
        ),
        migrations.CreateModel(
            name='TipoNotificacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=20, verbose_name='Título')),
                ('cor', colorfield.fields.ColorField(max_length=10)),
            ],
            options={
                'verbose_name': 'Tipo Notificação',
                'verbose_name_plural': 'Tipos Notificações',
            },
        ),
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('usuario_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sexo',
                 models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], default='Masculino',
                                  max_length=10)),
                ('datanascimento',
                 models.DateField(default=django.utils.timezone.now, verbose_name='Data de nascimento')),
                ('turma', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Aluno',
                'verbose_name_plural': 'Alunos',
            },
            bases=('notificacao.usuario',),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('remetente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notificacao.Remetente')),
                ('sigla', models.CharField(max_length=4, verbose_name='Sigla')),
                ('qtd_modulos', models.IntegerField(default=8, verbose_name='Módulos')),
                ('carga_horaria', models.IntegerField(default=3200, verbose_name='Carga horária')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
            },
            bases=('notificacao.remetente',),
        ),
        migrations.CreateModel(
            name='Instituto',
            fields=[
                ('remetente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notificacao.Remetente')),
                ('datafundacao',
                 models.DateField(blank=True, help_text='dd/mm/yyyy', null=True, verbose_name='Data de fundação')),
            ],
            options={
                'verbose_name': 'Instituto',
                'verbose_name_plural': 'Institutos',
            },
            bases=('notificacao.remetente',),
        ),
        migrations.CreateModel(
            name='Oferecimento',
            fields=[
                ('remetente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notificacao.Remetente')),
                ('ano',
                 models.IntegerField(choices=[(2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)],
                                     default=2017, verbose_name='year')),
                ('semestre', models.IntegerField(choices=[(1, 'Primeiro'), (2, 'Segundo')], default=1)),
                ('week',
                 models.IntegerField(choices=[(1, 'Segunda'), (2, 'Terça'), (3, 'Quarta'), (4, 'Quinta'), (5, 'Sexta')],
                                     default=1, verbose_name='Dia da semana')),
                ('time', models.IntegerField(
                    choices=[(1, 'Primeiro'), (2, 'Segundo'), (3, 'Terceiro'), (4, 'Quarto'), (5, 'Quinto')], default=1,
                    verbose_name='Horário')),
                ('qtd', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=2,
                                            verbose_name='Quantidade de aulas')),
                ('professor', models.CharField(default='Professor teste', max_length=61, verbose_name='Professor')),
                ('sigla', models.CharField(default='DDD', max_length=4, verbose_name='Sigla')),
                ('id_curso', models.IntegerField(default=0, verbose_name='Curso')),
                ('dataInicio', models.DateField(default=django.utils.timezone.now, verbose_name='Data Início')),
                ('alunos', models.ManyToManyField(blank=True, null=True, to='notificacao.Aluno')),
                ('id_disciplina', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Disciplina')),
            ],
            options={
                'verbose_name': 'Oferecimento',
                'verbose_name_plural': 'Oferecimentos',
            },
            bases=('notificacao.remetente',),
        ),
        migrations.CreateModel(
            name='SalaProfessores',
            fields=[
                ('remetente_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notificacao.Remetente')),
                ('id_curso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notificacao.Curso')),
            ],
            options={
                'verbose_name': 'Sala Professores',
                'verbose_name_plural': 'Salas Professores',
            },
            bases=('notificacao.remetente',),
        ),
        migrations.CreateModel(
            name='Servidor',
            fields=[
                ('usuario_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('sexo',
                 models.CharField(choices=[('Masculino', 'Masculino'), ('Feminino', 'Feminino')], default='Masculino',
                                  max_length=10)),
                ('datanascimento',
                 models.DateField(default=django.utils.timezone.now, verbose_name='Data de nascimento')),
                ('funcao', models.CharField(max_length=30, verbose_name='Função')),
                ('admin', models.BooleanField(default=False, verbose_name='Admin sistema')),
            ],
            options={
                'verbose_name': 'Servidor',
                'verbose_name_plural': 'Servidores',
            },
            bases=('notificacao.usuario',),
        ),
        migrations.CreateModel(
            name='Turma',
            fields=[
                ('remetente_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='notificacao.Remetente')),
                ('sigla', models.CharField(max_length=10)),
                ('id_curso', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE,
                                               to='notificacao.Curso')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turma',
            },
            bases=('notificacao.remetente',),
        ),
        migrations.AddField(
            model_name='remetente',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+',
                                    to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='id_tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.TipoNotificacao',
                                    verbose_name='Tipo notificação'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='remetente',
            field=models.ManyToManyField(to='notificacao.Remetente'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('servidor_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='notificacao.Servidor')),
                ('formacao', models.CharField(max_length=20, verbose_name='Área')),
                ('tipo_formacao', models.CharField(
                    choices=[('Técnico', 'Técnico'), ('Graduação', 'Graduação'), ('Pós Graduação', 'Pós Graduação'),
                             ('Mestrado', 'Mestrado'), ('Doutorado', 'Doutorado'), ('Pós Doutorado', 'Pós Doutorado'),
                             ('Livre Docência', 'Livre Docência')], default='Graduação', max_length=15,
                    verbose_name='Tipo formação')),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professores',
            },
            bases=('notificacao.servidor',),
        ),
        migrations.AddField(
            model_name='servidor',
            name='id_instituto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notificacao.Instituto'),
        ),
        migrations.AddField(
            model_name='notificacao',
            name='servidor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Servidor'),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='id_curso',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Curso',
                                    verbose_name='Curso'),
        ),
        migrations.AddField(
            model_name='curso',
            name='id_instituto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Instituto'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='id_instituto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='notificacao.Instituto'),
        ),
        migrations.AddField(
            model_name='aluno',
            name='pkTurma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Turma',
                                    verbose_name='Turma'),
        ),
        migrations.AddField(
            model_name='salaprofessores',
            name='professores',
            field=models.ManyToManyField(to='notificacao.Professor'),
        ),
        migrations.AddField(
            model_name='oferecimento',
            name='id_professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notificacao.Professor'),
        ),
        migrations.RunPython(apply_migration),
    ]
