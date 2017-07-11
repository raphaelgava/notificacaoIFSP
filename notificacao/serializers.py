from rest_framework import serializers

from .models import Aluno
from .models import Instituto
from .models import Notificacao
from .models import Pessoa
from .models import Professor
from .models import Remetente
from .models import Servidor
from .models import TipoNotificacao
from .models import Oferecimento
from .stuff.helpers import CreatePerson


class _PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        abstract = True
        fields = ('pk','username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto',)


class AlunoSerializer(_PessoaSerializer):
    class Meta:
        model = Aluno
        fields = _PessoaSerializer.Meta.fields + ('turma',)

    def create(self, validated_data):
        aluno = serializers.ModelSerializer.create(self, validated_data)
        password = validated_data['password']
        aluno = CreatePerson.create_student(aluno, password)

        return aluno


class ServidorSerializer(_PessoaSerializer):
    class Meta:
        model = Servidor
        fields = _PessoaSerializer.Meta.fields + ('funcao',)

    def create(self, validated_data, isProfessor=False):
        servidor = serializers.ModelSerializer.create(self, validated_data)
        password = validated_data['password']
        servidor = CreatePerson.create_employee(servidor, password, isProfessor)

        return servidor


class ProfessorSerializer(ServidorSerializer):
    class Meta:
        model = Professor
        fields = _PessoaSerializer.Meta.fields + ('formacao', 'tipo_formacao',)

    def create(self, validated_data):
        professor = ServidorSerializer.create(self, validated_data, True)
        return professor


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ('pk','datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'servidor', 'remetente')


class TipoNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNotificacao
        fields = ('pk','descricao', 'cor',)


class _RemetenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remetente
        abstract = True
        fields = ('pk','descricao',)


class InstitutoSerializer(_RemetenteSerializer):
    class Meta:
        model = Instituto
        fields = _RemetenteSerializer.Meta.fields + ('datafundacao',)

class OferecimentoSerializer(_RemetenteSerializer):
    class Meta:
        model = Oferecimento
        fields = _RemetenteSerializer.Meta.fields + ('ano', 'semestre', 'week', 'time', 'period', 'dataInicio', 'id_professor', 'id_disciplina')
