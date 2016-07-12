from django.contrib import admin
from .models import Aluno
from .models import Professor
from .models import Servidor
from .models import Curso
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Salaalunos
from .models import Salaprofessores
from .models import Tiponotificacao
from .models import Tipoformacao

# Register your models here.

admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Servidor)
admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Instituto)
admin.site.register(Local)
admin.site.register(Notificacao)
admin.site.register(Oferecimento)
admin.site.register(Salaalunos)
admin.site.register(Salaprofessores)
admin.site.register(Tiponotificacao)
admin.site.register(Tipoformacao)