from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from notificacao.forms import DisciplinaForm
from notificacao.forms import TipoNotificacaoForm
from notificacao.models import Disciplina
from notificacao.models import TipoNotificacao
from notificacao.stuff.constants import GroupConst, HTML, Urls
from .deleteAdd import AddItem, ApagarItem


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


# todo: não esta aparecendo cadastro disciplina no template de disciplina!!
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
    template_name = HTML.LISTA_DISCIPLINA

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
