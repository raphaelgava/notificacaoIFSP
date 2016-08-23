from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework import viewsets

from .forms import AlunoForm
from .forms import LoginForm
from .forms import ProfessorForm
from .forms import ServidorForm
from .models import Aluno
from .models import Notificacao
from .models import Professor
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao
from .models import Usuario
from .serializers import AlunoSerializer
from .serializers import NotificacaoSerializer
from .serializers import ProfessorSerializer
from .serializers import ServidorSerializer
from .serializers import TipoFormacaoSerializer
from .serializers import TipoNotificacaoSerializer
from .stuff.constants import GroupConst, HTML, Paginas, Mensagens, Urls
from .stuff.helpers import CreatePerson


def thanks(request):
    return render(request, HTML.THANKS)


class Logout(TemplateView):
    template_name = 'login.html'
    login_url = Paginas.LOGIN_URL

    def out(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(Paginas.LOGIN))

    def get(self, request, *args, **kwargs):
        # logout(request)
        # messages.info(request, 'Out', extra_tags='logged')
        # response = render(request, 'login.html')
        # response.set_cookie('logged', 'Out')
        # return response
        return self.out(request)

    def post(self, request, *args, **kwargs):
        return self.out(request)


class Login(TemplateView):
    template_name = 'login.html'
    login_url = Paginas.LOGIN_URL

    def checkUser(self, request, user):
        if user is not None:
            if user.is_active:
                # variable = "teste"
                # context = {
                #     'variable': variable,
                # }
                if user.groups.filter(name=GroupConst.STUDENT).count() == 1:
                    # messages.info(request, GroupConst.STUDENT)
                    # response = render(request, 'loginUsuario.html', {'bla': variable})
                    # response.set_cookie('logged', 'Estudante')
                    # return response
                    return HttpResponseRedirect(reverse('loginAluno'))
                elif user.groups.filter(name=GroupConst.EMPLOYEE).count() == 1:
                    return HttpResponseRedirect(reverse('loginServidor'))
                elif user.groups.filter(name=GroupConst.PROFESSOR).count() == 1:
                    return HttpResponseRedirect(reverse('loginProfessor'))
                elif user.groups.filter(name=GroupConst.ADMIN).count() == 1:
                    return HttpResponseRedirect(reverse('loginAdmin'))
                else:
                    logout(request)
            else:
                logout(request)

        messages.error(request, Mensagens.USUARIO_INVALIDO)
        return HttpResponseRedirect(reverse(Paginas.LOGIN))

    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None:
            if not user.is_anonymous():
                return self.checkUser(request, user)

        form = LoginForm()
        return render(request, HTML.LOGIN, {'form': form})

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.error(request, Mensagens.DADOS_INVALIDOS)
            return HttpResponseRedirect(reverse(Paginas.LOGIN))
            # return render(request, HTML.LOGIN, {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, Mensagens.LOGIN_INVALIDO)
            return HttpResponseRedirect(reverse(Paginas.LOGIN))
            # return render(request, HTML.LOGIN, {'form': form})

        # form.clean_remember_me(self);
        # remember = form.cleaned_data['remember_me']
        # if remember:
        #     request.session.set_expiry(1209600) # 2 weeks

        login(request, user)
        return self.checkUser(request, user)


# ==========================================PÁGINAS LOGIN===============================================================

class AlunoLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginUsuario.html'
    success_url = reverse_lazy('loginAluno')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.STUDENT]


class ServidorLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginUsuario.html'
    success_url = reverse_lazy('loginServidor')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.EMPLOYEE]


class ProfessorLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginUsuario.html'
    success_url = reverse_lazy('loginProfessor')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.PROFESSOR]


class AdminLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginUsuario.html'
    success_url = reverse_lazy('loginAdmin')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


#======================================================================================================================


# ==========================================CADASTRO ALUNO=============================================================
class CadastrarAluno(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO_ALUNO
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']

        if password == password_check:
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

            CreatePerson.create_student(aluno, password)

            return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_ALUNO))

        messages.error(self.request, Mensagens.DADOS_INVALIDOS)
        return render(self.request, HTML.CADASTRO_ALUNO, {'form': form})


    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarAluno, self).get_context_data(**kwargs)
        context['raphael'] = Aluno.objects.all()
        return context


class AtualizarAluno(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO_ALUNO
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        sexo = form.cleaned_data['sexo']
        datanascimento = form.cleaned_data['datanascimento']
        instituto = form.cleaned_data['id_instituto']
        turma = form.cleaned_data['turma']

        # aluno = Aluno.objects.get_or_create(username=username, password=password, email=email, first_name=first_name,
        #                              last_name=last_name,
        #                              sexo=sexo, datanascimento=datanascimento, id_instituto=instituto, turma=turma)

        aluno = Aluno.objects.filter(username=username).first()
        if password == password_check:
            if aluno is not None:
                aluno.email = email
                aluno.first_name = first_name
                aluno.last_name = last_name
                aluno.sexo = sexo
                aluno.datanascimento = datanascimento
                aluno.id_instituto = instituto
                aluno.turma = turma

                CreatePerson.create_student(aluno, password)
                return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_ALUNO))
            else:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
        else:
            if aluno is None:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
            messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')

        return render(self.request, HTML.CADASTRO_ALUNO, {'form': form})


class ApagarPessoa(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    template_name = HTML.DELETE
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_object(self, **kwargs):
        return Usuario.objects.filter(pk=self.kwargs.get('pk')).first()

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        success_url = self.get_success_url()
        if request.method == 'POST':
            if 'confirm' in request.POST:
                self.object = self.get_object()
                self.object.delete()
        return HttpResponseRedirect(success_url)


class ApagarAluno(ApagarPessoa, LoginRequiredMixin, GroupRequiredMixin):
    model = Aluno
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)


class AddPessoa(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = HTML.ADD
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_object(self, **kwargs):
        return Usuario.objects.filter(pk=self.kwargs.get('pk')).first()

    # def get_context_data(self, **kwargs):
    #     context = super(AddPessoa, self).get_context_data(**kwargs)
    #     context['teste'] = Usuario.objects.filter(pk=self.kwargs.get('pk')).first()
    #     return context

    def post(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        if request.method == 'POST':
            if 'confirm' in request.POST:
                usuario = self.get_object()
                usuario.activeAgain()
        return HttpResponseRedirect(success_url)


class AddAluno(AddPessoa, LoginRequiredMixin, GroupRequiredMixin):
    # template_name = HTML.ADD
    model = Aluno
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)

    # login_url = '/login/'

    # group_required = [GroupConst.ADMIN]

    # def get_object(self, **kwargs):
    #     return Usuario.objects.filter(pk=self.kwargs.get('pk')).first()
    #
    # def post(self, request, *args, **kwargs):
    #     success_url = self.get_success_url()
    #     if request.method == 'POST':
    #         if 'confirm' in request.POST:
    #             usuario = self.get_object()
    #             usuario.activeAgain()
    #     return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)


class ListarAlunos(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_ALUNO
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy('aluno')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarAlunos, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Aluno.objects.filter(is_active=True)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Aluno.objects.filter(is_active=False)
                        return context

        context['lista'] = Aluno.objects.all()
        return context


# ======================================================================================================================

# ==========================================CADASTRO SERVIDOR=============================================================

class CadastrarServidor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO_SERVIDOR
    model = Servidor
    form_class = ServidorForm
    success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']

        if password == password_check:
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            sexo = form.cleaned_data['sexo']
            datanascimento = form.cleaned_data['datanascimento']
            instituto = form.cleaned_data['id_instituto']
            funcao = form.cleaned_data['funcao']

            servidor = Servidor.objects.create(username=username, password=password, email=email, first_name=first_name,
                                               last_name=last_name,
                                               sexo=sexo, datanascimento=datanascimento, id_instituto=instituto,
                                               funcao=funcao)

            CreatePerson.create_student(servidor, password)

            return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_SERVIDOR))

        messages.error(self.request, Mensagens.DADOS_INVALIDOS)
        return render(self.request, HTML.CADASTRO_SERVIDOR, {'form': form})

    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarServidor, self).get_context_data(**kwargs)
        context['raphael'] = Servidor.objects.all()
        return context


class AtualizarServidor(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO_SERVIDOR
    model = Servidor
    form_class = ServidorForm
    success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        sexo = form.cleaned_data['sexo']
        datanascimento = form.cleaned_data['datanascimento']
        instituto = form.cleaned_data['id_instituto']
        funcao = form.cleaned_data['funcao']

        servidor = Servidor.objects.filter(username=username).first()
        if password == password_check:
            if servidor is not None:
                servidor.email = email
                servidor.first_name = first_name
                servidor.last_name = last_name
                servidor.sexo = sexo
                servidor.datanascimento = datanascimento
                servidor.id_instituto = instituto
                servidor.funcao = funcao

                CreatePerson.create_student(servidor, password)
                return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_SERVIDOR))
            else:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
        else:
            if servidor is None:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
            messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')

        return render(self.request, HTML.CADASTRO_SERVIDOR, {'form': form})


class ApagarServidor(ApagarPessoa, LoginRequiredMixin, GroupRequiredMixin):
    model = Servidor
    success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


class AddServidor(AddPessoa, LoginRequiredMixin, GroupRequiredMixin):
    model = Servidor
    success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


class ListarServidores(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_SERVIDOR
    model = Servidor
    form_class = ServidorForm
    success_url = reverse_lazy('servidor')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarServidores, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Servidor.objects.filter(is_active=True).exclude(funcao='Professor')
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Servidor.objects.filter(is_active=False).exclude(funcao='Professor')
                        return context

        context['lista'] = Servidor.objects.all().exclude(funcao='Professor')
        return context


# ======================================================================================================================


# ==========================================CADASTRO PROFESSOR=============================================================

class CadastrarProfessor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO_PROFESSOR
    model = Professor
    form_class = ProfessorForm
    success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']

        if password == password_check:
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            sexo = form.cleaned_data['sexo']
            datanascimento = form.cleaned_data['datanascimento']
            instituto = form.cleaned_data['id_instituto']
            funcao = 'Professor'
            id_tipo = form.cleaned_data['id_tipo']
            formacao = form.cleaned_data['formacao']

            professor = Professor.objects.create(username=username, password=password, email=email,
                                                 first_name=first_name,
                                                 last_name=last_name,
                                                 sexo=sexo, datanascimento=datanascimento, id_instituto=instituto,
                                                 funcao=funcao,
                                                 formacao=formacao, id_tipo=id_tipo)

            CreatePerson.create_student(professor, password)

            return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_PROFESSOR))

        messages.error(self.request, Mensagens.DADOS_INVALIDOS)
        return render(self.request, HTML.CADASTRO_PROFESSOR, {'form': form})

    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarProfessor, self).get_context_data(**kwargs)
        context['raphael'] = Professor.objects.all()
        return context


class AtualizarProfessor(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO_PROFESSOR
    model = Professor
    form_class = ProfessorForm
    success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def form_valid(self, form):
        form.save(commit=False)

        password = form.cleaned_data['password']
        password_check = form.cleaned_data['password_check']
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        email = form.cleaned_data['email']
        sexo = form.cleaned_data['sexo']
        datanascimento = form.cleaned_data['datanascimento']
        instituto = form.cleaned_data['id_instituto']
        # funcao = form.cleaned_data['funcao']
        id_tipo = form.cleaned_data['id_tipo']
        formacao = form.cleaned_data['formacao']

        professor = Professor.objects.filter(username=username).first()
        if password == password_check:
            if professor is not None:
                professor.email = email
                professor.first_name = first_name
                professor.last_name = last_name
                professor.sexo = sexo
                professor.datanascimento = datanascimento
                professor.id_instituto = instituto
                # professor.funcao = funcao
                professor.id_tipo = id_tipo
                professor.formacao = formacao

                CreatePerson.create_student(professor, password)
                return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_PROFESSOR))
            else:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
        else:
            if professor is None:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
            messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')

        return render(self.request, HTML.CADASTRO_PROFESSOR, {'form': form})


class ApagarProfessor(ApagarPessoa, LoginRequiredMixin, GroupRequiredMixin):
    model = Professor
    success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


class AddProfessor(AddPessoa, LoginRequiredMixin, GroupRequiredMixin):
    model = Professor
    success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


class ListarProfessores(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_PROFESSOR
    model = Professor
    form_class = ProfessorForm
    success_url = reverse_lazy('professor')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarProfessores, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Professor.objects.filter(is_active=True)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Professor.objects.filter(is_active=False)
                        return context

        context['lista'] = Professor.objects.all()
        return context


# ======================================================================================================================


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
        return Servidor.objects.all().exclude(
            funcao='Professor')  # todo: verificar se de fato aqui é necessario essa verificacao


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
