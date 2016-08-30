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
from .forms import DisciplinaForm
from .forms import InstitutoForm
from .forms import LoginForm
from .forms import ProfessorForm
from .forms import ServidorForm
from .forms import TipoNotificacaoForm
from .models import Aluno
from .models import Disciplina
from .models import Instituto
from .models import Notificacao
from .models import Professor
from .models import Remetente
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao
from .models import Usuario
from .serializers import AlunoSerializer
from .serializers import InstitutoSerializer
from .serializers import NotificacaoSerializer
from .serializers import ProfessorSerializer
from .serializers import ServidorSerializer
from .serializers import TipoFormacaoSerializer
from .serializers import TipoNotificacaoSerializer
from .stuff.constants import GroupConst, HTML, Paginas, Mensagens, Urls
from .stuff.helpers import CreatePerson


def thanks(request):
    return render(request, HTML.THANKS)


# todo: cadastro dos remetentes!!!!


class Logout(TemplateView):
    template_name = HTML.LOGIN
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
    template_name = HTML.LOGIN
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

        #todo: verificar o esquema de redirecionamento caso deslogar por tempo (ao acessar a url em que estava, sera pedido o login, após o login deve encaminhar para onde tava)

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
class UsuarioLogin(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = HTML.LOGIN_USUARIO
    login_url = Paginas.LOGIN_URL


class AlunoLogado(UsuarioLogin):
    # template_name = HTML.LOGIN_USUARIO
    success_url = reverse_lazy('loginAluno')
    # login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.STUDENT]


class ServidorLogado(UsuarioLogin):
    # template_name = HTML.LOGIN_USUARIO
    success_url = reverse_lazy('loginServidor')
    # login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.EMPLOYEE]


class ProfessorLogado(UsuarioLogin):
    # template_name = HTML.LOGIN_USUARIO
    success_url = reverse_lazy('loginProfessor')
    # login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.PROFESSOR]


class AdminLogado(UsuarioLogin):
    # template_name = HTML.LOGIN_USUARIO
    success_url = reverse_lazy('loginAdmin')
    # login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


#======================================================================================================================


# ==========================================ADD/DELETE ITEM============================================================


class ApagarItem(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    template_name = HTML.DELETE
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]

    #     http://reinout.vanrees.org/weblog/2014/05/19/context.html
    def get_object(self, **kwargs):
        return self.model.objects.filter(pk=self.kwargs.get('pk')).first()

    def get_class(self):
        if issubclass(self.model, Usuario):
            return 'Usuário'
        elif issubclass(self.model, Remetente):
            return 'Remetente'
        else:  # todo: verificar necessidade de isinstance(self.model, Disciplina) pois esse não esta conectado em nada!!!
            return 'Tipo'

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


class AddItem(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = HTML.ADD
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]

    def get_object(self, **kwargs):
        return self.model.objects.filter(pk=self.kwargs.get('pk')).first()

    # def get_context_data(self, **kwargs):
    #     context = super(AddPessoa, self).get_context_data(**kwargs)
    #     context['teste'] = Usuario.objects.filter(pk=self.kwargs.get('pk')).first()
    #     return context

    def get_class(self):
        if issubclass(self.model, Usuario):
            return 'Usuário'
        elif issubclass(self.model, Remetente):
            return 'Remetente'
        elif isinstance(self.model, Disciplina):
            return 'Disciplina'
        else:
            return 'Tipo'

    def post(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        if request.method == 'POST':
            if 'confirm' in request.POST:
                item = self.get_object()
                item.activeAgain()
        return HttpResponseRedirect(success_url)


# ======================================================================================================================

# ==========================================CADASTRO USUARIO=============================================================

class CadastrarUsuario(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


class AtualizarUsuario(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


class ListarUsuario(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_USUARIOS
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


#======================================================================================================================

# ==========================================CADASTRO ALUNO=============================================================

class AlunoView:
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)


# class CadastrarAluno(LoginRequiredMixin, GroupRequiredMixin, CreateView):
class CadastrarAluno(AlunoView, CadastrarUsuario):
    # template_name = HTML.CADASTRO
    # model = Aluno
    # form_class = AlunoForm
    # success_url = reverse_lazy(Urls.LISTAR_ALUNO)
    # login_url = '/login/'

    # group_required = [GroupConst.ADMIN]

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
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Aluno'


# class AtualizarAluno(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
class AtualizarAluno(AlunoView, AtualizarUsuario):
    # template_name = HTML.CADASTRO
    # model = Aluno
    # form_class = AlunoForm
    # success_url = reverse_lazy(Urls.LISTAR_ALUNO)
    # login_url = '/login/'
    #
    # group_required = [GroupConst.ADMIN]

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

        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Atualizar Aluno'


# class ApagarAluno(ApagarItem, LoginRequiredMixin, GroupRequiredMixin):
#     model = Aluno
#     success_url = reverse_lazy(Urls.LISTAR_ALUNO)
class ApagarAluno(AlunoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)

    # class AddAluno(AddItem, LoginRequiredMixin, GroupRequiredMixin):
    # template_name = HTML.ADD
    # model = Aluno
    # success_url = reverse_lazy(Urls.LISTAR_ALUNO)

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


class AddAluno(AlunoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)


# class ListarAlunos(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     template_name = HTML.LISTA_USUARIOS
#     model = Aluno
#     form_class = AlunoForm
#     success_url = reverse_lazy('aluno')
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class ListarAlunos(AlunoView, ListarUsuario):
    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (lista) para exibi-lo
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

    def get_title(self, **kwargs):
        return 'Cadastro Aluno'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_ALUNO

    def get_link_add(self, **kwargs):
        return Urls.ADD_ALUNO

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_ALUNO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_ALUNO


# ======================================================================================================================

# ==========================================CADASTRO SERVIDOR===========================================================

class ServidorView:
    model = Servidor
    form_class = ServidorForm
    success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)


# class CadastrarServidor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
#     template_name = HTML.CADASTRO
#     model = Servidor
#     form_class = ServidorForm
#     success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class CadastrarServidor(ServidorView, CadastrarUsuario):

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
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Servidor'


# class AtualizarServidor(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
#     template_name = HTML.CADASTRO
#     model = Servidor
#     form_class = ServidorForm
#     success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class AtualizarServidor(ServidorView, AtualizarUsuario):

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

        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Atualizar Servidor'


# class ApagarServidor(ApagarItem, LoginRequiredMixin, GroupRequiredMixin):
#     model = Servidor
#     success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
class ApagarServidor(ServidorView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


# class AddServidor(AddItem, LoginRequiredMixin, GroupRequiredMixin):
#     model = Servidor
#     success_url = reverse_lazy(Urls.LISTAR_SERVIDOR)
class AddServidor(ServidorView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


# class ListarServidores(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     template_name = HTML.LISTA_USUARIOS
#     model = Servidor
#     form_class = ServidorForm
#     success_url = reverse_lazy('servidor')
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class ListarServidores(ServidorView, ListarUsuario):
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

    def get_title(self, **kwargs):
        return 'Cadastro Servidor'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_SERVIDOR

    def get_link_add(self, **kwargs):
        return Urls.ADD_SERVIDOR

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_SERVIDOR

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_SERVIDOR


# ======================================================================================================================


# ==========================================CADASTRO PROFESSOR==========================================================
class ProfessorView:
    model = Professor
    form_class = ProfessorForm
    success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)


# class CadastrarProfessor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
#     template_name = HTML.CADASTRO
#     model = Professor
#     form_class = ProfessorForm
#     success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class CadastrarProfessor(ProfessorView, CadastrarUsuario):

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
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Professor'


# class AtualizarProfessor(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
#     template_name = HTML.CADASTRO
#     model = Professor
#     form_class = ProfessorForm
#     success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class AtualizarProfessor(ProfessorView, AtualizarUsuario):

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

        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Atualizar Professor'


# class ApagarProfessor(ApagarItem, LoginRequiredMixin, GroupRequiredMixin):
#     model = Professor
#     success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
class ApagarProfessor(ProfessorView, ApagarItem):

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


# class AddProfessor(AddItem, LoginRequiredMixin, GroupRequiredMixin):
#     model = Professor
#     success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
class AddProfessor(ProfessorView, AddItem):

    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


# class ListarProfessores(LoginRequiredMixin, GroupRequiredMixin, ListView):
#     template_name = HTML.LISTA_USUARIOS
#     model = Professor
#     form_class = ProfessorForm
#     success_url = reverse_lazy(Urls.LISTAR_PROFESSOR)
#     login_url = '/login/'
#
#     group_required = [GroupConst.ADMIN]
class ListarProfessores(ProfessorView, ListarUsuario):

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

    def get_title(self, **kwargs):
        return 'Cadastro Professor'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_PROFESSOR

    def get_link_add(self, **kwargs):
        return Urls.ADD_PROFESSOR

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_PROFESSOR

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_PROFESSOR


# ======================================================================================================================




# ==========================================CADASTRO REMETENTE==========================================================

class CadastrarRemetente(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]


class AtualizarRemetente(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]


class ListarRemetentes(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_REMETENTES
    success_url = reverse_lazy(HTML.LISTA_REMETENTES)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarRemetentes, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Remetente.objects.filter(is_active=True)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Remetente.objects.filter(is_active=False)
                        return context

        context['lista'] = Remetente.objects.all()
        return context


class InstitutoView:
    model = Instituto
    form_class = InstitutoForm
    success_url = reverse_lazy(Urls.LISTAR_INSTITUTO)


class CadastrarInstituto(InstitutoView, CadastrarRemetente):
    def get_title(self, **kwargs):
        return 'Cadastro Instituto (Remetente)'


class AtualizarInstituto(InstitutoView, AtualizarRemetente):
    def get_title(self, **kwargs):
        return 'Atualizar Instituto (Remetente)'


class ApagarInstituto(InstitutoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_INSTITUTO)


class AddInstituto(InstitutoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_INSTITUTO)


class ListarInstitutos(InstitutoView, ListarRemetentes):
    def get_title(self, **kwargs):
        return 'Cadastro Instituto (Remetente)'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_INSTITUTO

    def get_link_add(self, **kwargs):
        return Urls.ADD_INSTITUTO

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_INSTITUTO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_INSTITUTO


# ======================================================================================================================


# ==========================================CADASTRO OUTROS=============================================================
class DisciplinaView(LoginRequiredMixin, GroupRequiredMixin):
    model = Disciplina
    form_class = DisciplinaForm
    success_url = reverse_lazy(Urls.LISTAR_DISCIPLINA)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]


class CadastrarDisciplina(DisciplinaView, CreateView):
    template_name = HTML.CADASTRO

    def get_title(self, **kwargs):
        return 'Cadastro Disciplina'


class AtualizarDisciplina(DisciplinaView, UpdateView):
    template_name = HTML.CADASTRO

    def get_title(self, **kwargs):
        return 'Atualizar Disciplina'


class ApagarDisciplina(DisciplinaView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_DISCIPLINA)


class AddDisciplina(DisciplinaView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_DISCIPLINA)


class ListarDisciplinas(DisciplinaView, ListView):
    template_name = HTML.LISTA_OUTROS

    def get_context_data(self, **kwargs):
        context = super(ListarDisciplinas, self).get_context_data(**kwargs)

        context['lista'] = Disciplina.objects.all()
        return context

    def get_title(self, **kwargs):
        return 'Cadastro Disciplina'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_DISCIPLINA

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_DISCIPLINA


class CadastrarTipoNotificacao(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    success_url = reverse_lazy(Urls.LISTAR_TIPO_NOTIFICACAO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_title(self, **kwargs):
        return 'Cadastro Tipo Notificação'


class AtualizarTipoNotificacao(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    success_url = reverse_lazy(Urls.LISTAR_TIPO_NOTIFICACAO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_title(self, **kwargs):
        return 'Atualizar Tipo Notificação'


class ListarTiposNotificacao(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_OUTROS
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    success_url = reverse_lazy(Urls.LISTAR_TIPO_NOTIFICACAO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarTiposNotificacao, self).get_context_data(**kwargs)

        context['lista'] = TipoNotificacao.objects.all()
        return context

    def get_title(self, **kwargs):
        return 'Cadastro Tipo Notificação'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_TIPO_NOTIFICACAO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_TIPO_NOTIFICACAO


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
