from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView

from notificacao.forms import CursoForm
from notificacao.forms import InstitutoForm
from notificacao.forms import OferecimentoForm
from notificacao.forms import SalaProfessoresForm
from notificacao.forms import TurmaForm
from notificacao.models import Curso, Professor, Disciplina, Aluno
from notificacao.models import Instituto
from notificacao.models import Oferecimento
from notificacao.models import Remetente
from notificacao.models import SalaProfessores
from notificacao.models import Turma
from notificacao.stuff.constants import GroupConst, HTML, Urls, Paginas
from .deleteAdd import ApagarItem, AddItem, WarningItem


# ==========================================CADASTRO REMETENTE==========================================================

class CadastrarRemetente(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


class AtualizarRemetente(LoginRequiredMixin, GroupRequiredMixin, UpdateView):
    template_name = HTML.CADASTRO
    login_url = Paginas.LOGIN_URL

    group_required = [GroupConst.ADMIN]


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
                    context['lista'] = Remetente.objects.order_by('-pk').filter(is_active=True).select_subclasses(
                        self.model)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Remetente.objects.order_by('-pk').filter(is_active=False).select_subclasses(
                            self.model)
                        return context

        context['lista'] = Remetente.objects.order_by('-pk').select_subclasses(self.model)
        return context


class InstitutoView:
    model = Instituto
    form_class = InstitutoForm
    success_url = reverse_lazy(Urls.LISTAR_INSTITUTO)


# todo: data cadastro não pode ser igual ou maior que hoje!!! (não tem porque cadastrar um instituto/aniversario(usuario) amanha!!!)
class CadastrarInstituto(InstitutoView, CadastrarRemetente):
    def form_valid(self, form):
        inst = form.save(commit=True)
        inst.tipo = "Instituto"
        inst.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_INSTITUTO))

    def get_title(self, **kwargs):
        return 'Cadastro Instituto (Remetente)'


class AtualizarInstituto(InstitutoView, AtualizarRemetente):
    def form_valid(self, form):
        inst = form.save(commit=True)
        inst.tipo = "Instituto"
        inst.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_INSTITUTO))

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

    group_required = [GroupConst.ADMIN, GroupConst.PROFESSOR]


class CadastrarOferecimento(OferecimentoView, CadastrarRemetente):
    def form_valid(self, form):
        # offer = form.save(commit=False)
        prof = Professor.objects.filter(pk=self.request.user.id).first()  # self.kwargs.get('pk'))
        if (prof is not None):
            offer = form.save(commit=True)
            offer.tipo = "Oferecimento"

            offer.id_professor = prof
            offer.professor = prof.first_name + ' ' + prof.last_name
            disciplina = Disciplina.objects.get(pk=offer.id_disciplina.pk)
            offer.sigla = disciplina.sigla
            offer.id_curso = disciplina.id_curso.pk
            # prof = Professor.objects.get(pk=offer.id_professor)
            # offer.professor = prof.first_name + ' ' + prof.last_name
            # disciplina = Disciplina.objects.get(pk=offer.id_disciplina.pk)
            # offer.sigla = disciplina.sigla
            # offer.id_curso = disciplina.id_curso.pk

            offer.save()

            return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_OFERECIMENTO))
        return HttpResponseRedirect(reverse_lazy(Urls.WARNING_OFERECIMENTO))

    def get_title(self, **kwargs):
        return 'Cadastro Oferecimento (Remetente)'

        # def get_link_warning(self, **kwargs):
        #     return Urls.WARNING_OFERECIMENTO


class AtualizarOferecimento(OferecimentoView, AtualizarRemetente):
    def form_valid(self, form):
        # prof = Professor.objects.get(pk=offer.id_professor)
        # offer.professor = prof.first_name + ' ' + prof.last_name
        prof = Professor.objects.filter(pk=self.request.user.id).first()  # self.kwargs.get('pk'))
        if (prof is not None):
            offer = form.save(commit=True)
            offer.tipo = "Oferecimento"
            offer.id_professor = prof
            offer.professor = prof.first_name + ' ' + prof.last_name
            disciplina = Disciplina.objects.get(pk=offer.id_disciplina.pk)
            offer.sigla = disciplina.sigla
            offer.id_curso = disciplina.id_curso.pk

            # for aluno in offer.alunos.all():
            #     if (aluno is not None):
            #         conta = 1;
            offer.save()

            return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_OFERECIMENTO))
        return HttpResponseRedirect(reverse_lazy(Urls.WARNING_OFERECIMENTO))

    def get_title(self, **kwargs):
        return 'Atualizar Oferecimento (Remetente)'


class WarningOferecimento(OferecimentoView, WarningItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_OFERECIMENTO)

class ApagarOferecimento(OferecimentoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_OFERECIMENTO)


class AddOferecimento(OferecimentoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_OFERECIMENTO)


class ListarOferecimentos(OferecimentoView, ListarRemetentes):
    def get_context_data(self, **kwargs):
        context = super(ListarRemetentes, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            if 'filtro' in self.request.GET:
                parametro = self.request.GET['filtro']
                if parametro == 'ativo':
                    context['lista'] = Oferecimento.objects.order_by('-pk').filter(is_active=True,
                                                                                   id_professor=self.request.user.id)
                    return context
                else:
                    if parametro == 'inativo':
                        context['lista'] = Oferecimento.objects.order_by('-pk').filter(is_active=False,
                                                                                       id_professor=self.request.user.id)
                        return context

        context['lista'] = Oferecimento.objects.order_by('-pk').filter(id_professor=self.request.user.id)
        return context

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


class CursoView:
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy(Urls.LISTAR_CURSO)


class CadastrarCurso(CursoView, CadastrarRemetente):
    def form_valid(self, form):
        cur = form.save(commit=True)
        cur.tipo = "Curso"
        cur.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_CURSO))

    def get_title(self, **kwargs):
        return 'Cadastro Curso (Remetente)'


class AtualizarCurso(CursoView, AtualizarRemetente):
    def form_valid(self, form):
        cur = form.save(commit=True)
        cur.tipo = "Curso"
        cur.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_CURSO))

    def get_title(self, **kwargs):
        return 'Atualizar Curso (Remetente)'


class ApagarCurso(CursoView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_CURSO)


class AddCurso(CursoView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_CURSO)


class ListarCursos(CursoView, ListarRemetentes):
    def get_title(self, **kwargs):
        return 'Cadastro Curso (Remetente)'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_CURSO

    def get_link_add(self, **kwargs):
        return Urls.ADD_CURSO

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_CURSO

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_CURSO


class TurmaView:
    model = Turma
    form_class = TurmaForm
    success_url = reverse_lazy(Urls.LISTAR_TURMA)


class CadastrarTurma(TurmaView, CadastrarRemetente):
    def form_valid(self, form):
        tur = form.save(commit=True)
        tur.tipo = "Turma"
        tur.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_TURMA))

    def get_title(self, **kwargs):
        return 'Cadastro Turma (Remetente)'


class AtualizarTurma(TurmaView, AtualizarRemetente):
    def form_valid(self, form):
        turma = form.save(commit=True)
        turma.tipo = "Turma"
        alunos = Aluno.objects.filter(pkTurma=turma.pk)

        for a in alunos:
            a.turma = turma.sigla
            a.save()

        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_TURMA))

    def get_title(self, **kwargs):
        return 'Atualizar Turma (Remetente)'


class ApagarTurma(TurmaView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_TURMA)


class AddTurma(TurmaView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_TURMA)


class ListarTurma(TurmaView, ListarRemetentes):
    def get_title(self, **kwargs):
        return 'Cadastro Turma (Remetente)'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_TURMA

    def get_link_add(self, **kwargs):
        return Urls.ADD_TURMA

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_TURMA

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_TURMA


class SalaProfessoresView:
    model = SalaProfessores
    form_class = SalaProfessoresForm
    success_url = reverse_lazy(Urls.LISTAR_SALA_PROFESSORES)

    group_required = [GroupConst.ADMIN, GroupConst.PROFESSOR]


class CadastrarSalaProfessores(SalaProfessoresView, CadastrarRemetente):
    def form_valid(self, form):
        sala = form.save(commit=True)
        sala.tipo = "Sala Professores"
        sala.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_SALA_PROFESSORES))

    def get_title(self, **kwargs):
        return 'Cadastro Sala Professores (Remetente)'


class AtualizarSalaProfessores(SalaProfessoresView, AtualizarRemetente):
    def form_valid(self, form):
        sala = form.save(commit=True)
        sala.tipo = "Sala Professores"
        sala.save()
        return HttpResponseRedirect(reverse_lazy(Urls.LISTAR_SALA_PROFESSORES))

    def get_title(self, **kwargs):
        return 'Atualizar Sala Professores (Remetente)'


class ApagarSalaProfessores(SalaProfessoresView, ApagarItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SALA_PROFESSORES)


class AddSalaProfessores(SalaProfessoresView, AddItem):
    def get_success_url(self):
        return reverse_lazy(Urls.LISTAR_SALA_PROFESSORES)


class ListarSalaProfessores(SalaProfessoresView, ListarRemetentes):
    def get_title(self, **kwargs):
        return 'Cadastro Sala Professores (Remetente)'

    def get_link_insert(self, **kwargs):
        return Urls.CADASTRAR_SALA_PROFESSOR

    def get_link_add(self, **kwargs):
        return Urls.ADD_SALA_PROFESSOR

    def get_link_delete(self, **kwargs):
        return Urls.DELETAR_SALA_PROFESSOR

    def get_link_modify(self, **kwargs):
        return Urls.ATUALIZAR_SALA_PROFESSOR

# todo: verificar lucas como abrir uma nova janela para adicionar campo na janela ja aberta!!!! (como admin do django - exemplo add curso com a opção de add institudo dentro dele )!!!
# modal window

# ======================================================================================================================
