from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import DeleteView

from notificacao.models import Disciplina
from notificacao.models import Remetente
from notificacao.models import Usuario
from notificacao.stuff.constants import GroupConst, HTML, Paginas


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
        elif isinstance(self.model, Disciplina):
            return 'Disciplina'
        else:
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


class WarningItem(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = HTML.WARNING
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN, GroupConst.EMPLOYEE]

    # def get_object(self, **kwargs):
    #     return self.model.objects.filter(pk=self.kwargs.get('pk')).first()

    # def get_context_data(self, **kwargs):
    #     context = super(AddPessoa, self).get_context_data(**kwargs)
    #     context['teste'] = Usuario.objects.filter(pk=self.kwargs.get('pk')).first()
    #     return context

    def get_class(self):
        return 'Oferecimento'
        # if issubclass(self.model, Usuario):
        #     return 'Usuário'
        # elif issubclass(self.model, Remetente):
        #     return 'Remetente'
        # elif isinstance(self.model, Disciplina):
        #     return 'Disciplina'
        # else:
        #     return 'Tipo'

    def post(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        # if request.method == 'POST':
        #     if 'confirm' in request.POST:
        # item = self.get_object()
        # item.activeAgain()
        return HttpResponseRedirect(success_url)


        # ======================================================================================================================
