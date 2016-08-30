from rest_framework import serializers

from .models import Aluno
from .models import Instituto
from .models import Notificacao
from .models import Pessoa
from .models import Professor
from .models import Remetente
from .models import Servidor
from .models import TipoFormacao
from .models import TipoNotificacao
from .stuff.helpers import CreatePerson


class PessoaLoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pessoa
        fields = ('username', 'password')

class _PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        abstract = True
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto',)


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
        fields = _PessoaSerializer.Meta.fields + ('formacao', 'id_tipo',)

    def create(self, validated_data):
        professor = ServidorSerializer.create(self, validated_data, True)
        return professor


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ('datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'username', 'remetente')


class TipoFormacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoFormacao
        fields = ('descricao',)


class TipoNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoNotificacao
        fields = ('descricao', 'cor',)


class _RemetenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remetente
        abstract = True
        fields = ('descricao',)


class InstitutoSerializer(_RemetenteSerializer):
    class Meta:
        model = Instituto
        fields = _RemetenteSerializer.Meta.fields + ('datafundacao',)
