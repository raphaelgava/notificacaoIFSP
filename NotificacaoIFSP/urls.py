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
from notificacao.views.json import AlunoViewSet
from notificacao.views.json import InstitutoViewSet
from notificacao.views.json import NotificacaoViewSet
from notificacao.views.json import ProfessorViewSet
from notificacao.views.json import ServidorViewSet
from notificacao.views.json import TipoFormacaoViewSet
from notificacao.views.json import TipoNotificacaoViewSet
from notificacao.views.login import AdminLogado, ServidorLogado, ProfessorLogado, AlunoLogado
from notificacao.views.login import Login, Logout
from notificacao.views.outros import CadastrarDisciplina, AtualizarDisciplina, ListarDisciplinas, ApagarDisciplina, \
    AddDisciplina
from notificacao.views.outros import CadastrarTipoNotificacao, AtualizarTipoNotificacao, ListarTiposNotificacao
from notificacao.views.remetente import CadastrarInstituto, AtualizarInstituto, ListarInstitutos, ApagarInstituto, \
    AddInstituto
from notificacao.views.remetente import CadastrarOferecimento, AtualizarOferecimento, ListarOferecimentos, \
    ApagarOferecimento, AddOferecimento
from notificacao.views.usuario import CadastrarAluno, AtualizarAluno, ApagarAluno, ListarAlunos, AddAluno
from notificacao.views.usuario import CadastrarProfessor, AtualizarProfessor, ApagarProfessor, ListarProfessores, \
    AddProfessor
from notificacao.views.usuario import CadastrarServidor, AtualizarServidor, ApagarServidor, ListarServidores, \
    AddServidor

router = routers.DefaultRouter()
router.register(r'aluno_json', AlunoViewSet, base_name='aluno')
router.register(r'servidor_json', ServidorViewSet, base_name='servidor')
router.register(r'professor_json', ProfessorViewSet, base_name='professor')
router.register(r'notificacao_json', NotificacaoViewSet, base_name='notificacao')
router.register(r'tipo_formacao_json', TipoFormacaoViewSet, base_name='tipoformacao')
router.register(r'tipo_notificacao_json', TipoNotificacaoViewSet, base_name='tiponotificacao')
router.register(r'instituto_json', InstitutoViewSet, base_name='instituto')

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

                  url(r'lista_instituto/$', ListarInstitutos.as_view(), name=Urls.LISTAR_INSTITUTO),
                  url(r'cadastro_instituto/$', CadastrarInstituto.as_view(), name=Urls.CADASTRAR_INSTITUTO),
                  url(r'cadastro_instituto/(?P<pk>\d+)/$', AtualizarInstituto.as_view(), name=Urls.ATUALIZAR_INSTITUTO),
                  url(r'delete_instituto/(?P<pk>\d+)/$', ApagarInstituto.as_view(), name=Urls.DELETAR_INSTITUTO),
                  url(r'add_instituto/(?P<pk>\d+)/$', AddInstituto.as_view(), name=Urls.ADD_INSTITUTO),

                  url(r'lista_Oferecimentos/$', ListarOferecimentos.as_view(), name=Urls.LISTAR_OFERECIMENTO),
                  url(r'cadastro_oferecimento/$', CadastrarOferecimento.as_view(), name=Urls.CADASTRAR_OFERECIMENTO),
                  url(r'cadastro_oferecimento/(?P<pk>\d+)/$', AtualizarOferecimento.as_view(),
                      name=Urls.ATUALIZAR_OFERECIMENTO),
                  url(r'delete_oferecimento/(?P<pk>\d+)/$', ApagarOferecimento.as_view(),
                      name=Urls.DELETAR_OFERECIMENTO),
                  url(r'add_oferecimento/(?P<pk>\d+)/$', AddOferecimento.as_view(), name=Urls.ADD_OFERECIMENTO),

                  url(r'lista_disciplinas/$', ListarDisciplinas.as_view(), name=Urls.LISTAR_DISCIPLINA),
                  url(r'cadastro_disciplina/$', CadastrarDisciplina.as_view(), name=Urls.CADASTRAR_DISCIPLINA),
                  url(r'cadastro_disciplina/(?P<pk>\d+)/$', AtualizarDisciplina.as_view(),
                      name=Urls.ATUALIZAR_DISCIPLINA),
                  url(r'delete_disciplina/(?P<pk>\d+)/$', ApagarDisciplina.as_view(), name=Urls.DELETAR_DISCIPLINA),
                  url(r'add_disciplina/(?P<pk>\d+)/$', AddDisciplina.as_view(), name=Urls.ADD_DISCIPLINA),

                  url(r'lista_tipo_notificacao/$', ListarTiposNotificacao.as_view(), name=Urls.LISTAR_TIPO_NOTIFICACAO),
                  url(r'cadastro_tipo_notificacao/$', CadastrarTipoNotificacao.as_view(),
                      name=Urls.CADASTRAR_TIPO_NOTIFICACAO),
                  url(r'cadastro_tipo_notificacao/(?P<pk>\d+)/$', AtualizarTipoNotificacao.as_view(),
                      name=Urls.ATUALIZAR_TIPO_NOTIFICACAO),

                  url(r'aluno/$', AlunoLogado.as_view(), name='loginAluno'),
                  url(r'professor/$', ProfessorLogado.as_view(), name='loginProfessor'),
                  url(r'servidor/$', ServidorLogado.as_view(), name='loginServidor'),
                  url(r'administrador/$', AdminLogado.as_view(), name='loginAdmin'),

                  url(r'^login/$', Login.as_view(), name='login'),
                  url(r'^logout/$', Logout.as_view(), name='logout'),
                  url(r'^$', Login.as_view(), name='login')
              ] + router.urls
