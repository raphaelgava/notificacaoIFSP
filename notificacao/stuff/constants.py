# Groups
class GroupConst:
    STUDENT = 'Student'
    EMPLOYEE = 'Employee'
    PROFESSOR = 'Professor'
    ADMIN = 'Admin'


# Person data
class PersonConst:
    PASSWORD = 'password'


class Paginas:
    LOGIN = 'login'
    LOGIN_URL = '/login/'


class Urls:
    LISTAR_ALUNO = 'listaAlunos'
    CADASTRAR_ALUNO = 'cadastroAluno'
    ATUALIZAR_ALUNO = 'cadastroUpdateAluno'
    DELETAR_ALUNO = 'cadastroDeleteAluno'
    ADD_ALUNO = 'cadastroAddAluno'

    LISTAR_SERVIDOR = 'listaServidores'
    CADASTRAR_SERVIDOR = 'cadastroServidor'
    ATUALIZAR_SERVIDOR = 'cadastroUpdateServidor'
    DELETAR_SERVIDOR = 'cadastroDeleteServidor'
    ADD_SERVIDOR = 'cadastroAddServidor'

    LISTAR_PROFESSOR = 'listaProfessores'
    CADASTRAR_PROFESSOR = 'cadastroProfessor'
    ATUALIZAR_PROFESSOR = 'cadastroUpdateProfessor'
    DELETAR_PROFESSOR = 'cadastroDeleteProfessor'
    ADD_PROFESSOR = 'cadastroAddProfessor'

    LISTAR_INSTITUTO = 'listaInstitutos'
    CADASTRAR_INSTITUTO = 'cadastroInstituto'
    ATUALIZAR_INSTITUTO = 'cadastroUpdateInstituto'
    DELETAR_INSTITUTO = 'cadastroDeleteInstituto'
    ADD_INSTITUTO = 'cadastroAddInstituto'

    LISTAR_DISCIPLINA = 'listaDisciplinas'
    CADASTRAR_DISCIPLINA = 'cadastroDisciplina'
    ATUALIZAR_DISCIPLINA = 'cadastroUpdateDisciplina'
    DELETAR_DISCIPLINA = 'cadastroDeleteDisciplina'
    ADD_DISCIPLINA = 'cadastroAddDisciplina'

    LISTAR_TIPO_NOTIFICACAO = 'listaTiposNotificacao'
    CADASTRAR_TIPO_NOTIFICACAO = 'cadastroTipoNotificacao'
    ATUALIZAR_TIPO_NOTIFICACAO = 'cadastroUpdateTipoNotificacao'


class HTML:
    CADASTRO = 'cadastro.html'
    LISTA_USUARIOS = 'listaOpcoesUsuario.html'
    LISTA_REMETENTES = 'listaOpcoesRemetente.html'
    LISTA_OUTROS = 'listaOpcoesOutros.html'

    ADD = 'add.html'
    DELETE = 'delete.html'

    LOGIN_USUARIO = 'loginUsuario.html'
    LOGIN = 'login.html'
    THANKS = 'thanks.html'


class Mensagens:
    DADOS_INVALIDOS = 'Dados inválidos. Tente novamente.'
    LOGIN_INVALIDO = 'Prontuário ou senha inválida. Tente novamente.'
    USUARIO_INVALIDO = 'Usuário Inválido.'
