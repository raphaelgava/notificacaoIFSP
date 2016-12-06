from rest_framework import viewsets

from notificacao.models import Aluno
from notificacao.models import Instituto
from notificacao.models import Notificacao
from notificacao.models import Professor
from notificacao.models import Servidor
from notificacao.models import TipoNotificacao
from notificacao.models import Oferecimento
from notificacao.serializers import AlunoSerializer
from notificacao.serializers import InstitutoSerializer
from notificacao.serializers import NotificacaoSerializer
from notificacao.serializers import ProfessorSerializer
from notificacao.serializers import ServidorSerializer
from notificacao.serializers import TipoNotificacaoSerializer
from notificacao.serializers import OferecimentoSerializer
from notificacao.stuff.constants import GroupConst

# DESCOBRIR COMO FAZER A QUERY DE MANYPRAMANY (TALVEZ UTILIZAR UTILIZAR SELF.USER.PK)
# LEMBRAR DE DESCOMENTAR OS NOVOS CAMPOS EM OFERECIMENTO!!!
# PARA ATUALIZAR UM ITEM BASTA FAZER UM PUT POR JSON
# PARA FAZER A BUSCA POR PK BASTA PASSAR O PK NA URL (POR CONTA DO LOOKUP_FIELD)
# QUESTIONAR COMO FAZER O USERNAME SER BASEADO NA PK!

class OferecimentoViewSet(viewsets.ModelViewSet):
    model = Oferecimento
    lookup_field = 'pk'
    serializer_class = OferecimentoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name=GroupConst.STUDENT).exists():
            oferecimentos = Oferecimento.objects.filter(alunos__username = user.username)
        elif user.groups.filter(name=GroupConst.PROFESSOR).exists():
            oferecimentos = Oferecimento.objects.filter(id_professor__username = user.username)
        else:
            oferecimentos = ''

        return oferecimentos

        # oferecimentos = Oferecimento.objects.filter(alunos__username = user.username)
        #
        # for ofer in oferecimentos:
        #     if ofer.descricao == 'Computação':
        #         return Oferecimento.objects.filter(alunos__username="0000001")
        # return Oferecimento.objects.filter(alunos__username="0000002")
        # return Oferecimento.objects.filter(alunos__username=self.request.user.username).count()


class AlunoViewSet(viewsets.ModelViewSet):
    model = Aluno
    lookup_field = 'pk'
    serializer_class = AlunoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Aluno.objects.all()


class ServidorViewSet(viewsets.ModelViewSet):
    model = Servidor
    lookup_field = 'pk'
    serializer_class = ServidorSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):  # todo: verificar se de fato aqui é necessario essa verificacao!!!
        return Servidor.objects.all().exclude(funcao='Professor')


class ProfessorViewSet(viewsets.ModelViewSet):
    model = Professor
    lookup_field = 'pk'
    serializer_class = ProfessorSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Professor.objects.all()


class NotificacaoViewSet(viewsets.ModelViewSet):
    model = Notificacao
    lookup_field = 'pk'
    serializer_class = NotificacaoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notificacao.objects.all()


class TipoNotificacaoViewSet(viewsets.ModelViewSet):
    model = TipoNotificacao
    lookup_field = 'pk'
    serializer_class = TipoNotificacaoSerializer

    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TipoNotificacao.objects.all()


class InstitutoViewSet(viewsets.ModelViewSet):
    model = Instituto
    lookup_field = 'pk'
    serializer_class = InstitutoSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Instituto.objects.all()
