from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Aluno
from .models import Curso
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Professor
from .models import SalaAlunos
from .models import SalaProfessores
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao


# from .model.pessoas import Aluno
# from .model.remetentes import Curso
# from .model.outros import Disciplina
# from .model.remetentes import Instituto
# from .model.outros import Local
# from .model.outros import Notificacao
# from .model.remetentes import Oferecimento
# from .model.pessoas import Professor
# from .model.remetentes import SalaAlunos
# from .model.remetentes import SalaProfessores
# from .model.pessoas import Servidor
# from .model.outros import TipoFormacao
# from .model.outros import TipoNotificacao


# Register your model here.

class _PersonAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (('Outras Informações'), {'fields': ('sexo', 'datanascimento', 'id_instituto')}),
    )

    class Meta:
        abstract = True;


class AlunoAdmin(_PersonAdmin):
    fieldsets = _PersonAdmin.fieldsets + (
        (('Informações Aluno'), {'fields': ('turma',)}),
    )


class ServidorAdmin(_PersonAdmin):
    fieldsets = _PersonAdmin.fieldsets + (
        (('Informações Servidor'), {'fields': ('funcao',)}),
    )


class ProfessorAdmin(_PersonAdmin):
    fieldsets = ServidorAdmin.fieldsets + (
        (('Informações Professor'), {'fields': ('formacao', 'id_tipo',)}),
    )


admin.site.register(Aluno, AlunoAdmin)
admin.site.register(Professor, ProfessorAdmin)
admin.site.register(Servidor, ServidorAdmin)
admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Instituto)
admin.site.register(Local)
admin.site.register(Notificacao)
admin.site.register(Oferecimento)
admin.site.register(SalaAlunos)
admin.site.register(SalaProfessores)
admin.site.register(TipoNotificacao)
admin.site.register(TipoFormacao)
