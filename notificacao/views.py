from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
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
from .stuff.constants import GroupConst, HTML, Paginas, Mensagens
from .stuff.helpers import CreatePerson


def thanks(request):
    return render(request, HTML.THANKS)


# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse(Paginas.LOGIN))
#
#
def checkUser(request, user):
    if user is not None:
        if user.is_active:
            variable = "teste"
            context = {
                'variable': variable,
            }
            if user.groups.filter(name=GroupConst.STUDENT).count() == 1:
                messages.info(request, GroupConst.STUDENT)
                return HttpResponseRedirect(reverse('loginAluno'))
            elif user.groups.filter(name=GroupConst.EMPLOYEE).count() == 1:
                messages.info(request, GroupConst.EMPLOYEE)
                return HttpResponseRedirect(reverse('loginServidor'))
            elif user.groups.filter(name=GroupConst.PROFESSOR).count() == 1:
                messages.info(request, GroupConst.PROFESSOR)
                return HttpResponseRedirect(reverse('loginProfessor'))
            elif user.groups.filter(name=GroupConst.ADMIN).count() == 1:
                messages.info(request, GroupConst.ADMIN)
                return render(request, 'loginAdministrador.html', {'bla': variable})
                # return HttpResponseRedirect(reverse('loginAdmin'))
            else:
                logout(request)

    messages.error(request, Mensagens.USUARIO_INVALIDO)
    return HttpResponseRedirect(reverse(Paginas.LOGIN))


# def login_view(request):
#     if request.method == "GET":
#         user = request.user
#         if user is not None:
#             if not user.is_anonymous():
#                 return checkUser(request, user)
#         form = LoginForm()
#         return render(request, HTML.LOGIN, {'form': form})
#     elif request.method == "POST":
#         form = LoginForm(request.POST)
#         if not form.is_valid():
#             messages.error(request, Mensagens.DADOS_INVALIDOS)
#             return HttpResponseRedirect(reverse(Paginas.LOGIN))
#
#         username = form.cleaned_data['username']
#         password = form.cleaned_data['password']
#         user = authenticate(username=username,
#                             password=password)
#         if not user:
#             messages.error(request, Mensagens.LOGIN_INVALIDO)
#             return HttpResponseRedirect(reverse(Paginas.LOGIN))
#
#         # form.clean_remember_me(self);
#         # remember = form.cleaned_data['remember_me']
#         # if remember:
#         #     request.session.set_expiry(1209600) # 2 weeks
#
#         login(request, user)
#         return checkUser(request, user)
#
#         # user.groups.all()
#         # if user.groups.filter(name=GroupConst.STUDENT).count() == 1:
#         #     messages.info(request, GroupConst.STUDENT)
#         #     return HttpResponseRedirect(reverse('loginAluno'))
#         # elif user.groups.filter(name=GroupConst.EMPLOYEE).count() == 1:
#         #     messages.info(request, GroupConst.EMPLOYEE)
#         #     return HttpResponseRedirect(reverse('loginServidor'))
#         # elif user.groups.filter(name=GroupConst.PROFESSOR).count() == 1:
#         #     messages.info(request, GroupConst.PROFESSOR)
#         #     return HttpResponseRedirect(reverse('loginProfessor'))
#         # elif user.groups.filter(name=GroupConst.ADMIN).count() == 1:
#         #     messages.info(request, GroupConst.ADMIN)
#         #     return HttpResponseRedirect(reverse('loginAdmin'))
#         # else:
#         #     logout(request)
#         #     messages.error(request, Mensagens.USUARIO_INVALIDO)
#         #     return HttpResponseRedirect(reverse(Paginas.LOGIN))

class Logout(TemplateView):
    template_name = 'login.html'
    login_url = Paginas.LOGIN_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse(Paginas.LOGIN))

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse(Paginas.LOGIN))


class Login(TemplateView):
    template_name = 'login.html'
    login_url = Paginas.LOGIN_URL

    # def checkUser(request, user):
    #     if user is not None:
    #         if user.groups.filter(name=GroupConst.STUDENT).count() == 1:
    #             messages.info(request, GroupConst.STUDENT)
    #             return HttpResponseRedirect(reverse('loginAluno'))
    #         elif user.groups.filter(name=GroupConst.EMPLOYEE).count() == 1:
    #             messages.info(request, GroupConst.EMPLOYEE)
    #             return HttpResponseRedirect(reverse('loginServidor'))
    #         elif user.groups.filter(name=GroupConst.PROFESSOR).count() == 1:
    #             messages.info(request, GroupConst.PROFESSOR)
    #             return HttpResponseRedirect(reverse('loginProfessor'))
    #         elif user.groups.filter(name=GroupConst.ADMIN).count() == 1:
    #             messages.info(request, GroupConst.ADMIN)
    #             return HttpResponseRedirect(reverse('loginAdmin'))
    #         else:
    #             logout(request)
    #             messages.error(request, Mensagens.USUARIO_INVALIDO)
    #             return HttpResponseRedirect(reverse(Paginas.LOGIN))
    #
    def get(self, request, *args, **kwargs):
        user = request.user
        if user is not None:
            if not user.is_anonymous():
                return checkUser(request, user)

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

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, Mensagens.LOGIN_INVALIDO)
            return HttpResponseRedirect(reverse(Paginas.LOGIN))

        # form.clean_remember_me(self);
        # remember = form.cleaned_data['remember_me']
        # if remember:
        #     request.session.set_expiry(1209600) # 2 weeks

        login(request, user)
        return checkUser(request, user)


# ==========================================PÁGINAS LOGIN===============================================================

class AlunoLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'aluno.html'
    success_url = reverse_lazy('loginAluno')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.STUDENT]


class ServidorLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginServidor.html'
    success_url = reverse_lazy('loginServidor')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.EMPLOYEE]


class ProfessorLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'professor.html'
    success_url = reverse_lazy('loginProfessor')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.PROFESSOR]


class AdminLogado(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'loginAdministrador.html'
    success_url = reverse_lazy('loginAdministrador')
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


#======================================================================================================================



# ==========================================CADASTRO ALUNO=============================================================

class CadastrarAluno(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy('listaAlunos')
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

            return HttpResponseRedirect(reverse_lazy('listaAlunos'))

        messages.error(self.request, Mensagens.DADOS_INVALIDOS)
        return render(self.request, HTML.CADASTRO_ALUNO, {'form': form})


    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (raphael) para exibi-lo
    def get_context_data(self, **kwargs):
        context = super(CadastrarAluno, self).get_context_data(**kwargs)
        context['raphael'] = Aluno.objects.all()
        return context


class AtualizarAluno(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = 'cadastroAluno.html'
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy('listaAlunos')
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
                return HttpResponseRedirect(reverse_lazy('listaAlunos'))
            else:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
        else:
            if aluno is None:
                messages.error(self.request, Mensagens.USUARIO_INVALIDO, extra_tags='wrongUser')
            messages.error(self.request, Mensagens.DADOS_INVALIDOS, extra_tags='wrongPassword')

        return render(self.request, HTML.CADASTRO_ALUNO, {'form': form})


class ApagarAluno(LoginRequiredMixin, GroupRequiredMixin, DeleteView):
    template_name = 'delete.html'
    model = Aluno
    # form_class = AlunoForm
    success_url = reverse_lazy('listaAlunos')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    # def form_valid(self, form):
    #     if self.request.GET['cancel']:
    #         form.save(commit=False)

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

    def get_success_url(self):
        return reverse_lazy('listaAlunos')


class ListarAluno(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = 'listaAlunos.html'
    model = Aluno
    form_class = AlunoForm
    success_url = reverse_lazy('servidor')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

    def activePerson(self):
        return Aluno.objects.filter(is_active=True)
        # return super(ListarAluno, self).get_query_set().filter(is_active=True)

    def allPerson(self):
        return Aluno.objects.all()

    # joga no context todos os objetos de Aluno, então no html é utilizado esse context (listaPessoa) para exibi-lo
        # def get_context_data(self, **kwargs):
        #     context = super(ListarAluno, self).get_context_data(**kwargs)
        #     # return super(ContactActiveManager, self).get_query_set().filter(is_active=True)
        #     context['listaPessoa'] = Aluno.objects.all();
        #     return context
        # {% for pessoa in listaPessoa %}
        # {% if forloop.counter|divisibleby:2 %}
        # <tr class="success">
        # {% else %}
        # <tr class="info">
        # {% endif %}
        # <td>{{ pessoa.username }}</td>
        # <td>{{ pessoa.first_name }}</td>
        # <td>{{ pessoa.last_name }}</td>
        # <td>{{ pessoa.email }}</td>
        # {% block opcoesLista %}
        # {% endblock %}
        # </tr>
        # {% endfor %}


# ======================================================================================================================

class CadastrarServidor(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'cadastroServidor.html'
    model = Servidor
    form_class = ServidorForm
    # success_url = '/thanks/'
    success_url = reverse_lazy('listaAluno')
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]

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
