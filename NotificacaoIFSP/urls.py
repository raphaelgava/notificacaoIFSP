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

from notificacao.stuff.constants import Urls
from notificacao.views import AdminLogado, ServidorLogado, ProfessorLogado, AlunoLogado
from notificacao.views import AlunoViewSet
from notificacao.views import CadastrarAluno, AtualizarAluno, ApagarAluno, ListarAlunos, AddAluno
from notificacao.views import CadastrarProfessor, AtualizarProfessor, ApagarProfessor, ListarProfessores, AddProfessor
from notificacao.views import CadastrarServidor, AtualizarServidor, ApagarServidor, ListarServidores, AddServidor
from notificacao.views import NotificacaoViewSet
from notificacao.views import ProfessorViewSet
from notificacao.views import ServidorViewSet
from notificacao.views import TipoFormacaoViewSet
from notificacao.views import TipoNotificacaoViewSet
from notificacao.views import thanks, Login, Logout

router = routers.DefaultRouter()
router.register(r'aluno_json', AlunoViewSet, base_name='aluno')
router.register(r'servidor_json', ServidorViewSet, base_name='servidor')
router.register(r'professor_json', ProfessorViewSet, base_name='professor')
router.register(r'notificacao_json', NotificacaoViewSet, base_name='notificacao')
router.register(r'tipo_formacao_json', TipoFormacaoViewSet, base_name='tipoformacao')
router.register(r'tipo_notificacao_json', TipoNotificacaoViewSet, base_name='tiponotificacao')

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'lista_aluno/$', ListarAlunos.as_view(), name=Urls.LISTAR_ALUNO),
                  url(r'cadastro_aluno/$', CadastrarAluno.as_view(), name=Urls.CADASTRAR_ALUNO),
                  url(r'cadastro_aluno/(?P<pk>\d+)/$', AtualizarAluno.as_view(), name=Urls.ATUALIZAR_ALUNO),
                  url(r'delete_aluno/(?P<pk>\d+)/$', ApagarAluno.as_view(), name=Urls.DELETAR_ALUNO),
                  url(r'add_aluno/(?P<pk>\d+)/$', AddAluno.as_view(), name=Urls.ADD_ALUNO),

                  url(r'lista_servidor/$', ListarServidores.as_view(), name=Urls.LISTAR_SERVIDOR),
                  url(r'cadastro_servidor/$', CadastrarServidor.as_view(), name=Urls.CADASTRAR_SERVIDOR),
                  url(r'cadastro_servidor/(?P<pk>\d+)/$', AtualizarServidor.as_view(), name=Urls.ATUALIZAR_SERVIDOR),
                  url(r'delete_servidor/(?P<pk>\d+)/$', ApagarServidor.as_view(), name=Urls.DELETAR_SERVIDOR),
                  url(r'add_servidor/(?P<pk>\d+)/$', AddServidor.as_view(), name=Urls.ADD_SERVIDOR),

                  url(r'lista_professor/$', ListarProfessores.as_view(), name=Urls.LISTAR_PROFESSOR),
                  url(r'cadastro_professor/$', CadastrarProfessor.as_view(), name=Urls.CADASTRAR_PROFESSOR),
                  url(r'cadastro_professor/(?P<pk>\d+)/$', AtualizarProfessor.as_view(), name=Urls.ATUALIZAR_PROFESSOR),
                  url(r'delete_professor/(?P<pk>\d+)/$', ApagarProfessor.as_view(), name=Urls.DELETAR_PROFESSOR),
                  url(r'add_professor/(?P<pk>\d+)/$', AddProfessor.as_view(), name=Urls.ADD_PROFESSOR),

                  url(r'aluno/$', AlunoLogado.as_view(), name='loginAluno'),
                  url(r'professor/$', ProfessorLogado.as_view(), name='loginProfessor'),
                  url(r'servidor/$', ServidorLogado.as_view(), name='loginServidor'),
                  url(r'administrador/$', AdminLogado.as_view(), name='loginAdmin'),

                  url(r'^login/$', Login.as_view(), name='login'),
                  url(r'^logout/$', Logout.as_view(), name='logout'),
                  url(r'^$', thanks, name="thanks")
              ] + router.urls
