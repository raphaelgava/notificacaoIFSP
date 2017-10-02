from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from notificacao.models import Aluno
from notificacao.models import Instituto
from notificacao.models import Notificacao
from notificacao.models import Oferecimento
from notificacao.models import Professor
from notificacao.models import Servidor
from notificacao.models import TipoNotificacao
from notificacao.serializers import AlunoSerializer
from notificacao.serializers import InstitutoSerializer
from notificacao.serializers import NotificacaoSerializer
from notificacao.serializers import OferecimentoSerializer
from notificacao.serializers import ProfessorSerializer
from notificacao.serializers import ServidorSerializer
from notificacao.serializers import TipoNotificacaoSerializer


# DESCOBRIR COMO FAZER A QUERY DE MANYPRAMANY (TALVEZ UTILIZAR UTILIZAR SELF.USER.PK)
# LEMBRAR DE DESCOMENTAR OS NOVOS CAMPOS EM OFERECIMENTO!!!
# PARA ATUALIZAR UM ITEM BASTA FAZER UM PUT POR JSON
# PARA FAZER A BUSCA POR PK BASTA PASSAR O PK NA URL (POR CONTA DO LOOKUP_FIELD)

class OferecimentoViewSet(viewsets.ModelViewSet):
    model = Oferecimento
    lookup_field = 'pk'
    serializer_class = OferecimentoSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (
    TokenAuthentication,)  # Agora para acessar o json tem que enviar o token na authorization do http!!!

    def get_queryset(self):
        # user = self.request.user
        # if user.groups.filter(name=GroupConst.STUDENT).exists():
        #     oferecimentos = Oferecimento.objects.filter(alunos__username = user.username)
        # elif user.groups.filter(name=GroupConst.PROFESSOR).exists():
        #     oferecimentos = Oferecimento.objects.filter(id_professor__username = user.username)
        # else:
        #     oferecimentos = ''

        ano = self.request.GET.get('ano')
        semestre = self.request.GET.get('semestre')
        if ano is not None and semestre is not None:
            oferecimentos = Oferecimento.objects.filter(ano=ano, semestre=semestre)
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

class PessoaViewSet(viewsets.ModelViewSet):
    lookup_field = 'pk'
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

class AlunoViewSet(PessoaViewSet):
    model = Aluno
    serializer_class = AlunoSerializer

    def get_queryset(self):
        return Aluno.objects.all()


class ServidorViewSet(PessoaViewSet):
    model = Servidor
    serializer_class = ServidorSerializer

    def get_queryset(self):  # todo: verificar se de fato aqui é necessario essa verificacao!!!
        return Servidor.objects.all().exclude(funcao='Professor')


class ProfessorViewSet(PessoaViewSet):
    model = Professor
    serializer_class = ProfessorSerializer

    def get_queryset(self):
        return Professor.objects.all()


class NotificacaoViewSet(viewsets.ModelViewSet):
    model = Notificacao
    lookup_field = 'pk'
    serializer_class = NotificacaoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Notificacao.objects.all()


class TipoNotificacaoViewSet(viewsets.ModelViewSet):
    model = TipoNotificacao
    lookup_field = 'pk'
    serializer_class = TipoNotificacaoSerializer
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return TipoNotificacao.objects.all()


class InstitutoViewSet(viewsets.ModelViewSet):
    model = Instituto
    lookup_field = 'pk'
    serializer_class = InstitutoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Instituto.objects.all()
