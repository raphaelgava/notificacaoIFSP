from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework import viewsets

from .forms import AlunoForm
from .forms import LoginForm
from .forms import ServidorForm
from .models import Aluno
from .models import Notificacao
from .models import Professor
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao
from .serializers import AlunoSerializer
from .serializers import NotificacaoSerializer
from .serializers import ProfessorSerializer
from .serializers import ServidorSerializer
from .serializers import TipoFormacaoSerializer
from .serializers import TipoNotificacaoSerializer
from .stuff.constants import GroupConst
from .stuff.helpers import CreatePerson


def thanks(request):
    return render(request, 'thanks.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponse('Invalid data')

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username,
                            password=password)
        if not user:
            return HttpResponse('Invalid username and/or password')

        login(request, user)

        # user.groups.all()
        if user.groups.filter(name=GroupConst.STUDENT).count() == 1:
            return HttpResponseRedirect(reverse('cadastroAluno'))
        elif user.groups.filter(name=GroupConst.EMPLOYEE).count() == 1:
            return HttpResponseRedirect(reverse('cadastroServidor'))
        elif user.groups.filter(name=GroupConst.ADMIN).count() == 1:
            return HttpResponseRedirect(reverse('cadastroAluno'))
        else:
            logout(request)
            return HttpResponse('Invalid group!!!')


class ListarAluno(ListView):
    template_name = 'aluno_list.html'
    model = Aluno


class CadastrarAluno(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = [GroupConst.STUDENT]

    def form_valid(self, form):
        # aluno = form.save(commit=False)
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']

        if password != password_check:
            return HttpResponse('Confirmação de senha inválida')

        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        sexo = form.cleaned_data['sexo']
        datanascimento = form.cleaned_data['datanascimento']
        instituto = form.cleaned_data['id_instituto']
        turma = form.cleaned_data['turma']

        aluno = Aluno.objects.create(username=username, password=password, email=email, first_name=first_name,
                                     last_name=last_name,
                                     sexo=sexo, datanascimento=datanascimento, id_instituto=instituto, turma=turma)

        # aluno.set_password(password)
        # aluno.save()
        # aluno = CreatePerson.create_student(aluno, password)
        CreatePerson.create_student(aluno, password)

        return HttpResponseRedirect(reverse('thanks'))

    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarAluno, self).get_context_data(**kwargs)
        context['raphael'] = Aluno.objects.all()
        return context


class AtualizarAluno(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = [GroupConst.STUDENT]


class CadastrarServidor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'cadastroServidor.html'
    model = Servidor
    form_class = ServidorForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = [GroupConst.EMPLOYEE]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']

        if password != password_check:
            return HttpResponse('Confirmação de senha inválida')

        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        sexo = form.cleaned_data['sexo']
        datanascimento = form.cleaned_data['datanascimento']
        instituto = form.cleaned_data['id_instituto']
        funcao = form.cleaned_data['funcao']

        aluno = Servidor.objects.create(username=username, password=password, email=email, first_name=first_name,
                                        last_name=last_name,
                                        sexo=sexo, datanascimento=datanascimento, id_instituto=instituto, funcao=funcao)

        # aluno.set_password(password)
        # aluno.save()
        CreatePerson.create_employee(aluno, password)

        return HttpResponseRedirect(reverse('thanks'))

    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarServidor, self).get_context_data(**kwargs)
        context['raphael'] = Servidor.objects.all()
        return context


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

    def get_queryset(self):
        return Servidor.objects.all()


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
