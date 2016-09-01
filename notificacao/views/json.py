from rest_framework import viewsets

from notificacao.models import Aluno
from notificacao.models import Instituto
from notificacao.models import Notificacao
from notificacao.models import Professor
from notificacao.models import Servidor
from notificacao.models import TipoFormacao
from notificacao.models import TipoNotificacao
from notificacao.serializers import AlunoSerializer
from notificacao.serializers import InstitutoSerializer
from notificacao.serializers import NotificacaoSerializer
from notificacao.serializers import ProfessorSerializer
from notificacao.serializers import ServidorSerializer
from notificacao.serializers import TipoFormacaoSerializer
from notificacao.serializers import TipoNotificacaoSerializer


# All objects
class AlunoViewSet(viewsets.ModelViewSet):
    model = Aluno
    lookup_field = 'pk'
    serializer_class = AlunoSerializer

    def get_queryset(self):
        return Aluno.objects.all()


class ServidorViewSet(viewsets.ModelViewSet):
    model = Servidor
    lookup_field = 'pk'
    serializer_class = ServidorSerializer

    def get_queryset(self):  # todo: verificar se de fato aqui é necessario essa verificacao!!!
        return Servidor.objects.all().exclude(funcao='Professor')


class ProfessorViewSet(viewsets.ModelViewSet):
    model = Professor
    lookup_field = 'pk'
    serializer_class = ProfessorSerializer

    def get_queryset(self):
        return Professor.objects.all()


class NotificacaoViewSet(viewsets.ModelViewSet):
    model = Notificacao
    lookup_field = 'pk'
    serializer_class = NotificacaoSerializer

    def get_queryset(self):
        return Notificacao.objects.all()


class TipoFormacaoViewSet(viewsets.ModelViewSet):
    model = TipoFormacao
    lookup_field = 'pk'
    serializer_class = TipoFormacaoSerializer

    def get_queryset(self):
        return TipoFormacao.objects.all()


class TipoNotificacaoViewSet(viewsets.ModelViewSet):
    model = TipoNotificacao
    lookup_field = 'pk'
    serializer_class = TipoNotificacaoSerializer

    def get_queryset(self):
        return TipoNotificacao.objects.all()


class InstitutoViewSet(viewsets.ModelViewSet):
    model = Instituto
    lookup_field = 'pk'
    serializer_class = InstitutoSerializer

    def get_queryset(self):
        return Instituto.objects.all()