from rest_framework import viewsets

from .serializers import AlunoSerializer
from .serializers import ServidorSerializer
from .serializers import ProfessorSerializer
from .serializers import TipoFormacaoSerializer
from .serializers import TipoNotificacaoSerializer

from .models import Aluno
from .models import Servidor
from .models import Professor
from .models import Tipoformacao
from .models import Tiponotificacao


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

    def get_queryset(self):
        return Servidor.objects.all()


class ProfessorViewSet(viewsets.ModelViewSet):
    model = Professor
    lookup_field = 'pk'
    serializer_class = ProfessorSerializer

    def get_queryset(self):
        return Professor.objects.all()


class TipoFormacaoViewSet(viewsets.ModelViewSet):
    model = Tipoformacao
    lookup_field = 'pk'
    serializer_class = TipoFormacaoSerializer

    def get_queryset(self):
        return Tipoformacao.objects.all()


class TipoNotificacaoViewSet(viewsets.ModelViewSet):
    model = Tiponotificacao
    lookup_field = 'pk'
    serializer_class = TipoNotificacaoSerializer

    def get_queryset(self):
        return Tiponotificacao.objects.all()
