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

# Register your models here.


admin.site.register(Aluno, UserAdmin)
admin.site.register(Professor, UserAdmin)
admin.site.register(Servidor, UserAdmin)
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
