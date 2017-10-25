# Groups
class GroupConst:
    STUDENT = 'Student'
    EMPLOYEE = 'Employee'
    PROFESSOR = 'Professor'
    ADMIN = 'Admin'


# Person data
class PersonConst:
    PASSWORD = 'password'
    PASSWORD_LENGTH = 5


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

    LISTAR_OFERECIMENTO = 'listaOferecimentos'
    CADASTRAR_OFERECIMENTO = 'cadastroOferecimento'
    ATUALIZAR_OFERECIMENTO = 'cadastroUpdateOferecimento'
    DELETAR_OFERECIMENTO = 'cadastroDeleteOferecimento'
    ADD_OFERECIMENTO = 'cadastroAddOferecimento'
    WARNING_OFERECIMENTO = 'cadastroWarningOferecimento'

    LISTAR_CURSO = 'listaCursos'
    CADASTRAR_CURSO = 'cadastroCurso'
    ATUALIZAR_CURSO = 'cadastroUpdateCurso'
    DELETAR_CURSO = 'cadastroDeleteCurso'
    ADD_CURSO = 'cadastroAddCurso'

    LISTAR_TURMA = 'listaTurma'
    CADASTRAR_TURMA = 'cadastroTurma'
    ATUALIZAR_TURMA = 'cadastroUpdateTurma'
    DELETAR_TURMA = 'cadastroDeleteTurma'
    ADD_TURMA = 'cadastroAddTurma'

    LISTAR_SALA_PROFESSORES = 'listaSalaProfessores'
    CADASTRAR_SALA_PROFESSOR = 'cadastroSalaProfessor'
    ATUALIZAR_SALA_PROFESSOR = 'cadastroUpdateSalaProfessor'
    DELETAR_SALA_PROFESSOR = 'cadastroDeleteSalaProfessor'
    ADD_SALA_PROFESSOR = 'cadastroAddSalaProfessor'

    LISTAR_DISCIPLINA = 'listaDisciplinas'
    CADASTRAR_DISCIPLINA = 'cadastroDisciplina'
    ATUALIZAR_DISCIPLINA = 'cadastroUpdateDisciplina'
    DELETAR_DISCIPLINA = 'cadastroDeleteDisciplina'
    ADD_DISCIPLINA = 'cadastroAddDisciplina'

    LISTAR_NOTIFICACAO = 'listaNotificacoes'
    CADASTRAR_NOTIFICACAO = 'cadastroNotificacao'
    ATUALIZAR_NOTIFICACAO = 'cadastroUpdateNotificacao'
    DELETAR_NOTIFICACAO = 'cadastroDeleteNotificacao'
    ADD_NOTIFICACAO = 'cadastroAddNotificacao'

    LISTAR_LOCAL = 'listaLocais'
    CADASTRAR_LOCAL = 'cadastroLocal'
    ATUALIZAR_LOCAL = 'cadastroUpdateLocal'

    LISTAR_TIPO_NOTIFICACAO = 'listaTiposNotificacao'
    CADASTRAR_TIPO_NOTIFICACAO = 'cadastroTipoNotificacao'
    ATUALIZAR_TIPO_NOTIFICACAO = 'cadastroUpdateTipoNotificacao'


class HTML:
    CADASTRO = 'cadastro.html'
    LISTA_USUARIOS = 'listaOpcoesUsuario.html'
    LISTA_REMETENTES = 'listaOpcoesRemetente.html'
    LISTA_TIPOS = 'listaOpcoesTipo.html'
    LISTA_OUTROS = 'listaOpcoesOutro.html'

    ADD = 'add.html'
    DELETE = 'delete.html'
    WARNING = 'warning.html'

    LOGIN_USUARIO = 'loginUsuario.html'
    LOGIN = 'index.html'
    THANKS = 'thanks.html'


class Mensagens:
    DADOS_INVALIDOS = 'Dados inválidos. Tente novamente.'
    LOGIN_INVALIDO = 'Prontuário ou senha inválida. Tente novamente.'
    USUARIO_INVALIDO = 'Usuário Inválido.'
