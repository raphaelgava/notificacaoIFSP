from rest_framework import viewsets

from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from .serializers import AlunoSerializer
from .serializers import AlunoLoginSerializer
from .serializers import ServidorSerializer
from .serializers import ProfessorSerializer
from .serializers import NotificacaoSerializer
from .serializers import TipoFormacaoSerializer
from .serializers import TipoNotificacaoSerializer

from .models import Aluno
from .models import Servidor
from .models import Professor
from .models import Notificacao
from .models import Tipoformacao
from .models import Tiponotificacao

from .forms import AlunoForm

def thanks(request):
    return render(request, 'thanks.html')

def login_user(request):
    logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/cadastro_aluno/')
    return render_to_response('login.html', context_instance=RequestContext(request))

class AlunoViewSet(viewsets.ModelViewSet):
    model = Aluno
    lookup_field = 'pk'
    serializer_class = AlunoSerializer

    def get_queryset(self):
        return Aluno.objects.all()

class AlunoLoginViewSet(viewsets.ModelViewSet):
    model = Aluno
    lookup_field = 'pk'
    serializer_class = AlunoLoginSerializer

    def get_queryset(self):
        return Aluno.objects.all()

class lista_aluno(ListView):
    template_name = 'aluno_list.html'
    model = Aluno

class cadastro_aluno(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = ["Servidores"]

    def form_valid(self, form):
        aluno = form.save(commit=False)

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
        aluno.set_password(password)

        aluno.save()
        return HttpResponseRedirect(reverse('thanks'))

    #joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(cadastro_aluno, self).get_context_data(**kwargs)
        context['raphael'] = Aluno.objects.all()
        return context

class cadastro_atualizar_aluno(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = ["Servidores"]


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
