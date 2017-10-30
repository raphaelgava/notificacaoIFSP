import datetime
from datetime import datetime

from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from notificacao.models import Aluno, Turma, Remetente, Local, SalaProfessores
from notificacao.models import Instituto
from notificacao.models import Notificacao
from notificacao.models import Oferecimento
from notificacao.models import Professor
from notificacao.models import Servidor
from notificacao.models import TipoNotificacao
from notificacao.serializers import AlunoSerializer, _RemetenteSerializer, LocalSerializer
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
        oferecimentos = None
        if self.request.method == "GET":
            ano = self.request.GET.get('ano')
            semestre = self.request.GET.get('semestre')
            pkTurma = self.request.GET.get('turma')
            pk = self.request.GET.get('pk')
            if ano is not None and semestre is not None:
                # if (pk is not None):
                #     oferecimentos = Oferecimento.objects.filter(ano=ano, semestre=semestre)
                #     for oferecimento in oferecimentos:
                #         aluno = oferecimento.alunos.filter(pk=pk).first()
                #         if (aluno is None):
                #             oferecimentos = oferecimentos.exclude(pk=oferecimento.pk)
                # else:
                if (pkTurma is None):
                    oferecimentos = Oferecimento.objects.filter(ano=ano, semestre=semestre)
                else:
                    turma = Turma.objects.get(pk=pkTurma)
                    oferecimentos = Oferecimento.objects.filter(ano=ano, semestre=semestre, id_curso=turma.id_curso.pk)
                    # else:
                    #     if (pkTurma is not None):
                    #         oferecimentos = Oferecimento.objects.filter(pk=pk)
                    #     else:
                    #         oferecimentos = ''
        else:
            if self.request.method == "PUT":
                oferecimentos = Oferecimento.objects.all()

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

    def get_queryset(self):
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
        notify = set()  # resultado
        hoje = datetime.today()
        notificacoes = Notificacao.objects.filter(datahora__gte=hoje)
        if self.request.method == "GET":
            if notificacoes is not None:
                id = self.request.GET.get('pk')
                user = self.request.GET.get('user')
                if id is not None and user is not None:
                    id = int(id)

                    # RAISING INSTITUTO - EVERYBORY
                    instituto = Instituto.objects.filter(is_active=True)
                    for noti in notificacoes:
                        remover = False;
                        for remet in noti.remetente.all():
                            for inst in instituto:
                                if inst.pk == remet.pk:
                                    pessoa = None
                                    if (user == '1'):
                                        pessoa = Aluno.objects.filter(id_instituto=inst.pk, pk=id).first()
                                    else:
                                        pessoa = Servidor.objects.filter(id_instituto=inst.pk, pk=id).first()

                                    if pessoa is not None:
                                        notify.add(noti)
                                        remover = True;
                                        break;
                            if remover == True:
                                break;
                        if remover == True:
                            notificacoes = notificacoes.exclude(pk=noti.pk)

                    # RAISING OFERECIMENTO - ALUNO AND PROFESSOR
                    if ((user == '1') or (user == '3')):
                        semestre = 1
                        if (hoje.month > 6):
                            semestre = 2

                        oferecimentos = Oferecimento.objects.filter(is_active=True, ano=hoje.year, semestre=semestre)

                        for noti in notificacoes:
                            remover = False;
                            for remet in noti.remetente.all():
                                for offer in oferecimentos:
                                    if (remet.pk == offer.pk):
                                        if (user == '1'):
                                            for al in offer.alunos.all():
                                                if al.pk == id:
                                                    notify.add(noti)
                                                    remover = True;
                                                    break;
                                        else:
                                            if (offer.id_professor_id == id):
                                                notify.add(noti)
                                                remover = True;
                                                break;
                                    if remover == True:
                                        break;
                                if remover == True:
                                    break;

                            if remover == True:
                                notificacoes = notificacoes.exclude(pk=noti.pk)

                    if (user == '1'):
                        # RAISING TRUMA/CURS0 - ALUNO
                        pessoa = Aluno.objects.filter(id=id).first()
                        for noti in notificacoes:
                            remover = False;
                            for remet in noti.remetente.all():
                                if pessoa.pkTurma_id == remet.pk:
                                    notify.add(noti)
                                    remover = True;
                                    break;
                                else:
                                    turma = Turma.objects.filter(id=pessoa.pkTurma_id).first()
                                    if turma is not None:
                                        if turma.id_curso_id == remet.pk:
                                            notify.add(noti)
                                            remover = True;
                                            break;

                            if remover == True:
                                notificacoes = notificacoes.exclude(pk=noti.pk)
                    elif (user == '3'):
                        # RAISING SALA - PROFESSOR
                        salas = SalaProfessores.objects.filter(is_active=True)
                        for noti in notificacoes:
                            remover = False;
                            for remet in noti.remetente.all():
                                for sala in salas:
                                    if (remet.pk == sala.pk):
                                        for pro in sala.professores.all():
                                            if pro.pk == id:
                                                notify.add(noti)
                                                remover = True;
                                                break;
                                    if remover == True:
                                        break;
                            if remover == True:
                                notificacoes = notificacoes.exclude(pk=noti.pk)

        return notify
        #return notificacoes
        # return Notificacao.objects.all()


class TipoNotificacaoViewSet(viewsets.ModelViewSet):
    model = TipoNotificacao
    lookup_field = 'pk'
    serializer_class = TipoNotificacaoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return TipoNotificacao.objects.all()


class LocalViewSet(viewsets.ModelViewSet):
    model = Local
    lookup_field = 'pk'
    serializer_class = LocalSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Local.objects.all()


class InstitutoViewSet(viewsets.ModelViewSet):
    model = Instituto
    lookup_field = 'pk'
    serializer_class = InstitutoSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Instituto.objects.all()


class RemetenteViewSet(viewsets.ModelViewSet):
    model = Remetente
    lookup_field = 'pk'
    serializer_class = _RemetenteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Remetente.objects.filter(is_active=True)
