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
#     url(r'^admin/', admin.site.urls),
# ]

from django.conf.urls import patterns, url
from django.contrib import admin
from rest_framework import routers

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
] + router.urls

# from django.conf.urls import patterns, url
# from django.contrib import admin
# from rest_framework import routers
# from notificacao.views import TipoFormacaoViewSet
#
# router = routers.DefaultRouter()
# router.register(r'tipo_formacao', TipoFormacaoViewSet, base_name='tipoformacao')
#
# urlpatterns = patterns('',
#
# ) + router.urls
