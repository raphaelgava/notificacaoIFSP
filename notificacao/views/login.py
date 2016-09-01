from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView

from notificacao.forms import LoginForm
from notificacao.stuff.constants import GroupConst, HTML, Paginas, Mensagens


class Logout(TemplateView):
    template_name = HTML.LOGIN
    login_url = Paginas.LOGIN_URL

    def out(self, request):
        logout(request)
        return HttpResponseRedirect(reverse(Paginas.LOGIN))

    def get(self, request, *args, **kwargs):
        # logout(request)
        # messages.info(request, 'Out', extra_tags='logged')
        # response = render(request, 'index.html')
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

        # todo: verificar o esquema de redirecionamento caso deslogar por tempo (ao acessar a url em que estava, sera pedido o login, após o login deve encaminhar para onde tava)

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

        login(request, user)
        return self.checkUser(request, user)


# ==========================================PÁGINAS LOGIN===============================================================
class UsuarioLogin(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = HTML.LOGIN_USUARIO
    login_url = Paginas.LOGIN_URL


class AlunoLogado(UsuarioLogin):
    success_url = reverse_lazy('loginAluno')
    group_required = [GroupConst.STUDENT]


class ServidorLogado(UsuarioLogin):
    success_url = reverse_lazy('loginServidor')
    group_required = [GroupConst.EMPLOYEE]


class ProfessorLogado(UsuarioLogin):
    success_url = reverse_lazy('loginProfessor')
    group_required = [GroupConst.PROFESSOR]


class AdminLogado(UsuarioLogin):
    success_url = reverse_lazy('loginAdmin')
    group_required = [GroupConst.ADMIN]

# ======================================================================================================================
