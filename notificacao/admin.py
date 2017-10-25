from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Aluno
from .models import Curso
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Professor
from .models import SalaProfessores
from .models import Servidor
from .models import TipoNotificacao
from .models import Turma

TokenAdmin.raw_id_fields = ('user',)

# Register your model here.

class _PersonAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (('Outras Informações'), {'fields': ('sexo', 'cpf', 'datanascimento', 'id_instituto',)}),
    )

    class Meta:
        abstract = True;


class AlunoAdmin(_PersonAdmin):
    fieldsets = _PersonAdmin.fieldsets + (
        (('Informações Aluno'), {'fields': ('pkTurma',)}),
    )


class ServidorAdmin(_PersonAdmin):
    fieldsets = _PersonAdmin.fieldsets + (
        (('Informações Servidor'), {'fields': ('funcao', 'admin',)}),
    )


class ProfessorAdmin(_PersonAdmin):
    fieldsets = ServidorAdmin.fieldsets + (
        (('Informações Professor'), {'fields': ('formacao', 'tipo_formacao',)}),
    )


# Isso foi feito para não aparecer o Content Type (utilizado no model) como combobox no admin do django
class _RemetenteAdmin(admin.ModelAdmin):
    fieldsets = (('Informações Remetente'), {'fields': ('descricao', 'is_active',)}),

    class Meta:
        abstract = True;


class InstitutoAdmin(_RemetenteAdmin):
    fieldsets = _RemetenteAdmin.fieldsets + (
        (('Informações Instituto'), {'fields': ('datafundacao',)}),
    )


class CursoAdmin(_RemetenteAdmin):
    fieldsets = _RemetenteAdmin.fieldsets + (
        (('Informações Curso'), {'fields': ('id_instituto', 'sigla', 'qtd_modulos', 'carga_horaria',)}),
    )

# class DisciplinaAdmin(_RemetenteAdmin):
#     fieldsets = _RemetenteAdmin.fieldsets + (
#         (('Informações Disciplina'), {'fields': ('descricao', 'sigla', 'id_curso')}),
#     )


class OferecimentoAdmin(_RemetenteAdmin):
    fieldsets = _RemetenteAdmin.fieldsets + (
        # (('Informações Oferecimento'), {'fields': ('ano', 'semestre', 'week', 'time', 'period', 'dataInicio', 'id_professor', 'id_disciplina', 'alunos')}),
        (('Informações Oferecimento'), {'fields': (
            # 'ano', 'semestre', 'week', 'time', 'dataInicio', 'id_professor', 'id_disciplina', 'alunos',)}),
            'ano', 'semestre', 'week', 'time', 'dataInicio', 'id_professor', 'id_disciplina',)}),
    )


class TurmaAdmin(_RemetenteAdmin):
    fieldsets = _RemetenteAdmin.fieldsets + (
        # (('Informações Turma'), {'fields': ('id_curso', 'alunos')}),
        (('Informações Turma'), {'fields': ('id_curso', 'sigla',)}),
    )


class SalaProfessoresAdmin(_RemetenteAdmin):
    fieldsets = _RemetenteAdmin.fieldsets + (
        (('Informações Sala Professores'), {'fields': ('id_curso', 'professores',)}),
    )


# class OferecimentoAlunosAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (('Informações'), {'fields': ('id_aluno', 'id_oferecimento',)}),
#     )


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Disciplina)
admin.site.register(Instituto, InstitutoAdmin)
admin.site.register(Local)
admin.site.register(Notificacao)
# admin.site.register(OferecimentoAlunos)#, OferecimentoAlunosAdmin)
admin.site.register(Oferecimento, OferecimentoAdmin)
admin.site.register(Turma, TurmaAdmin)
admin.site.register(SalaProfessores, SalaProfessoresAdmin)
admin.site.register(TipoNotificacao)
