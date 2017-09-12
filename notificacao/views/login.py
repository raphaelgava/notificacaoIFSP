import datetime

from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from notificacao.forms import LoginForm
from notificacao.stuff.constants import GroupConst, HTML, Paginas, Mensagens


class MyObtainAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        utc_now = datetime.datetime.utcnow()
        if not created and token.created < utc_now - datetime.timedelta(
                minutes=15):  # token de 24 horas de duração -> hours=24
            token.delete()
            token = Token.objects.create(user=user)
            token.created = datetime.datetime.utcnow()
            token.save()

        prof = False
        if user.is_active == True:
            # groups.values_list('name', flat=True).first()
            name = 'NONE'
            if user.groups.filter(Q(name=GroupConst.PROFESSOR) | Q(name=GroupConst.PROFESSOR) | Q(
                    name=GroupConst.STUDENT) | Q(name=GroupConst.ADMIN)).exists():
                name = user.groups.all()[0].name

            if name == GroupConst.ADMIN:
                prof = user.isProfessor(user)
            else:
                if name == GroupConst.PROFESSOR:
                    prof = True

            return Response({'token': token.key, 'id': token.user_id, 'group': name, 'prof': prof})
        return Response({'token': token.key, 'id': '', 'group': '', 'prof': prof})

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
