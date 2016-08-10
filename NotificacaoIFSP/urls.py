"""NotificacaoIFSP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin
#
# urlpatterns = [
#     url(r'^cadastro/', admin.site.urls),
# ]

from django.conf.urls import url
from django.contrib import admin
from rest_framework import routers

from notificacao.views import AdminLogado, ServidorLogado, ProfessorLogado, AlunoLogado
from notificacao.views import AlunoViewSet
from notificacao.views import CadastrarAluno, AtualizarAluno, ListarAluno
from notificacao.views import CadastrarServidor
from notificacao.views import NotificacaoViewSet
from notificacao.views import ProfessorViewSet
from notificacao.views import ServidorViewSet
from notificacao.views import TipoFormacaoViewSet
from notificacao.views import TipoNotificacaoViewSet
from notificacao.views import login_view, logout_view, thanks

router = routers.DefaultRouter()
router.register(r'aluno_json', AlunoViewSet, base_name='aluno')
router.register(r'servidor_json', ServidorViewSet, base_name='servidor')
router.register(r'professor_json', ProfessorViewSet, base_name='professor')
router.register(r'notificacao_json', NotificacaoViewSet, base_name='notificacao')
router.register(r'tipo_formacao_json', TipoFormacaoViewSet, base_name='tipoformacao')
router.register(r'tipo_notificacao_json', TipoNotificacaoViewSet, base_name='tiponotificacao')

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'lista_aluno/$', ListarAluno.as_view(), name='listaAlunos'),
                  url(r'cadastro_aluno/$', CadastrarAluno.as_view(), name='cadastroAluno'),
                  url(r'cadastro_aluno/(?P<pk>\d+)/$', AtualizarAluno.as_view(), name='cadastroUpdateAluno'),

                  url(r'cadastro_servidor/$', CadastrarServidor.as_view(), name='cadastroServidor'),

                  url(r'aluno/$', AlunoLogado.as_view(), name='loginAluno'),
                  url(r'professor/$', ProfessorLogado.as_view(), name='loginProfessor'),
                  url(r'servidor/$', ServidorLogado.as_view(), name='loginServidor'),
                  url(r'administrador/$', AdminLogado.as_view(), name='loginAdmin'),

                  url(r'^login/$', login_view, name='login'),
                  url(r'^logout/$', logout_view, name='logout'),
                  url(r'^$', thanks, name="thanks")
              ] + router.urls
