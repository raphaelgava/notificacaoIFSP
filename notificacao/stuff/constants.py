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


class HTML:
    CADASTRO_ALUNO = 'cadastroAluno.html'
    CADASTRO_SERVIDOR = 'cadastroServidor.html'
    CADASTRO_PROFESSOR = 'cadastroProfessor.html'

    LISTA_ALUNO = 'listaAlunos.html'
    LISTA_SERVIDOR = 'listaServidores.html'
    LISTA_PROFESSOR = 'listaProfessores.html'

    ADD = 'add.html'
    DELETE = 'delete.html'

    LOGIN = 'login.html'
    THANKS = 'thanks.html'


class Mensagens:
    DADOS_INVALIDOS = 'Dados inválidos. Tente novamente.'
    LOGIN_INVALIDO = 'Prontuário ou senha inválida. Tente novamente.'
    USUARIO_INVALIDO = 'Usuário Inválido.'
