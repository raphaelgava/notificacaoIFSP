from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from notificacao.forms import InstitutoForm
from notificacao.forms import OferecimentoForm
from notificacao.models import Instituto
from notificacao.models import Oferecimento
from notificacao.models import Remetente
from notificacao.stuff.constants import GroupConst, HTML, Urls, Paginas
from .deleteAdd import ApagarItem, AddItem


# ==========================================CADASTRO REMETENTE==========================================================

class CadastrarRemetente(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


class AtualizarRemetente(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


# todo: tornar todos os campos UPPERCASE
class ListarRemetentes(LoginRequiredMixin, GroupRequiredMixin, ListView):
    template_name = HTML.LISTA_REMETENTES
    success_url = reverse_lazy(HTML.LISTA_REMETENTES)
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]

    def get_context_data(self, **kwargs):
        context = super(ListarRemetentes, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Remetente.objects.filter(is_active=True).select_subclasses(self.model)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Remetente.objects.filter(is_active=False).select_subclasses(self.model)
                        return context

        context['lista'] = Remetente.objects.select_subclasses(self.model)
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


class OferecimentoView:
    model = Oferecimento
    form_class = OferecimentoForm
    success_url = reverse_lazy(Urls.LISTAR_OFERECIMENTO)


class CadastrarOferecimento(OferecimentoView, CadastrarRemetente):
    def get_title(self, **kwargs):
        return 'Cadastro Oferecimento (Remetente)'


class AtualizarOferecimento(OferecimentoView, AtualizarRemetente):
    def get_title(self, **kwargs):
        return 'Atualizar Oferecimento (Remetente)'


class ApagarOferecimento(OferecimentoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_OFERECIMENTO)


class AddOferecimento(OferecimentoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_OFERECIMENTO)


class ListarOferecimentos(OferecimentoView, ListarRemetentes):
    def get_title(self, **kwargs):
        return 'Cadastro Oferecimento (Remetente)'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_OFERECIMENTO

    def get_link_add(self, **kwargs):
        return Urls.ADD_OFERECIMENTO

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_OFERECIMENTO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_OFERECIMENTO

# ======================================================================================================================
