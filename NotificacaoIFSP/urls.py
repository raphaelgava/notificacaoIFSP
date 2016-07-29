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

from notificacao.views import CadastrarAluno, AtualizarAluno, ListarAluno
from notificacao.views import CadastrarServidor

# from notificacao.views import login_user, thanks
from notificacao.views import login_view, logout_view, thanks

from notificacao.views import AlunoViewSet
from notificacao.views import ServidorViewSet
from notificacao.views import ProfessorViewSet
from notificacao.views import NotificacaoViewSet
from notificacao.views import TipoFormacaoViewSet
from notificacao.views import TipoNotificacaoViewSet

router = routers.DefaultRouter()
router.register(r'aluno', AlunoViewSet, base_name='aluno')
router.register(r'servidor', ServidorViewSet, base_name='servidor')
router.register(r'professor', ProfessorViewSet, base_name='professor')
router.register(r'notificacao', NotificacaoViewSet, base_name='notificacao')
router.register(r'tipo_formacao', TipoFormacaoViewSet, base_name='tipoformacao')
router.register(r'tipo_notificacao', TipoNotificacaoViewSet, base_name='tiponotificacao')

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'lista_aluno/$', ListarAluno.as_view(), name='listaAluno'),
                  url(r'cadastro_aluno/$', CadastrarAluno.as_view(), name='cadastroAluno'),
                  url(r'cadastro_aluno/(?P<pk>\d+)/$', AtualizarAluno.as_view(), name='cadastroUpdateAluno'),
                  url(r'cadastro_servidor/$', CadastrarServidor.as_view(), name='cadastroServidor'),
                  # url(r'^login/$', login_user),
                  url(r'^login/$', login_view, name='login'),
                  url(r'^logout/$', logout_view, name='logout'),
                  url(r'^$', thanks, name="thanks")
              ] + router.urls
