from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from notificacao.forms import DisciplinaForm
from notificacao.forms import LocalForm
from notificacao.forms import NotificacaoForm
from notificacao.forms import TipoNotificacaoForm
from notificacao.models import Disciplina
from notificacao.models import Local
from notificacao.models import Notificacao
from notificacao.models import TipoNotificacao
from notificacao.stuff.constants import GroupConst, HTML, Urls
from .deleteAdd import AddItem, ApagarItem


class NotificacaoView(LoginRequiredMixin, GroupRequiredMixin):
    model = Notificacao
    form_class = NotificacaoForm
    success_url = reverse_lazy(Urls.LISTAR_NOTIFICACAO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN, GroupConst.EMPLOYEE, GroupConst.PROFESSOR]


class CadastrarNotificacao(NotificacaoView, CreateView):
    template_name = HTML.CADASTRO

    def get_title(self, **kwargs):
        return 'Cadastro Notificação'


class AtualizarNotificacao(NotificacaoView, UpdateView):
    template_name = HTML.CADASTRO

    def get_title(self, **kwargs):
        return 'Atualizar Notificação'


class ApagarNotificacao(NotificacaoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_NOTIFICACAO)


class AddNotificacao(NotificacaoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_NOTIFICACAO)


class ListarNotificacoes(NotificacaoView, ListView):
    template_name = HTML.LISTA_OUTROS

    def get_context_data(self, **kwargs):
        context = super(ListarNotificacoes, self).get_context_data(**kwargs)

        context['lista'] = Notificacao.objects.all()
        return context

    def get_title(self, **kwargs):
        return 'Cadastro Notificação'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_NOTIFICACAO

    def get_link_add(self, **kwargs):
        return Urls.ADD_NOTIFICACAO

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_NOTIFICACAO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_NOTIFICACAO


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

    def get_link_add(self, **kwargs):
        return Urls.ADD_DISCIPLINA

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_DISCIPLINA

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_DISCIPLINA


class LocalView(LoginRequiredMixin, GroupRequiredMixin):
    template_name = HTML.CADASTRO
    model = Local
    form_class = LocalForm
    success_url = reverse_lazy(Urls.LISTAR_LOCAL)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]


# todo: procurar por APAGAR DEPOIS nos htmls!!!

# todo: como manter o efeito do hover da classe well quando acessar a página?

class CadastrarLocal(LocalView, CreateView):
    def get_title(self, **kwargs):
        return 'Cadastro Local'


class AtualizarLocal(LocalView, UpdateView):
    def get_title(self, **kwargs):
        return 'Atualizar Local'


class ListarLocal(LocalView, ListView):
    template_name = HTML.LISTA_TIPOS

    def get_context_data(self, **kwargs):
        context = super(ListarLocal, self).get_context_data(**kwargs)

        context['lista'] = Local.objects.all()
        return context

    def get_title(self, **kwargs):
        return 'Cadastro Local'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_LOCAL

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_LOCAL


class TipoNotificacaoView(LoginRequiredMixin, GroupRequiredMixin):
    template_name = HTML.CADASTRO
    model = TipoNotificacao
    form_class = TipoNotificacaoForm
    success_url = reverse_lazy(Urls.LISTAR_TIPO_NOTIFICACAO)
    login_url = '/login/'

    group_required = [GroupConst.ADMIN]


class CadastrarTipoNotificacao(TipoNotificacaoView, CreateView):
    def get_title(self, **kwargs):
        return 'Cadastro Tipo Notificação'


class AtualizarTipoNotificacao(TipoNotificacaoView, UpdateView):
    def get_title(self, **kwargs):
        return 'Atualizar Tipo Notificação'


class ListarTiposNotificacao(TipoNotificacaoView, ListView):
    template_name = HTML.LISTA_TIPOS

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
