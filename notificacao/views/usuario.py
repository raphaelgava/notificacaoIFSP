from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from notificacao.forms import AlunoForm
from notificacao.forms import ProfessorForm
from notificacao.forms import ServidorForm
from notificacao.models import Aluno
from notificacao.models import Professor
from notificacao.models import Servidor
from notificacao.stuff.constants import GroupConst, HTML, Paginas, Mensagens, Urls
from notificacao.stuff.helpers import CreatePerson
from .deleteAdd import AddItem, ApagarItem


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
    # success_url = reverse_lazy(HTML.LISTA_USUARIOS) #todo: verificar nas classes o success_url (alguns com HTML outros sem nada)
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


# ======================================================================================================================

# ==========================================CADASTRO ALUNO=============================================================

class AlunoView:
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy(Urls.LISTAR_ALUNO)


class CadastrarAluno(AlunoView, CadastrarUsuario):
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

        messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Aluno'


class AtualizarAluno(AlunoView, AtualizarUsuario):
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


class ApagarAluno(AlunoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)


class AddAluno(AlunoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_ALUNO)


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

        messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Servidor'


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


class ApagarServidor(ServidorView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


class AddServidor(ServidorView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SERVIDOR)


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

        messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')
        return render(self.request, HTML.CADASTRO, {'form': form})

    def get_title(self, **kwargs):
        return 'Cadastrar Professor'


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


class ApagarProfessor(ProfessorView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


class AddProfessor(ProfessorView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_PROFESSOR)


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