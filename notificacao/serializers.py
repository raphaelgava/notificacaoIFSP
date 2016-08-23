from rest_framework import serializers

from .models import Aluno
from .models import Notificacao
from .models import Pessoa
from .models import Professor
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

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = _PessoaSerializer.Meta.fields + ('turma',)

    def create(self, validated_data):
        aluno = serializers.ModelSerializer.create(self, validated_data)
        password = validated_data['password']
        aluno = CreatePerson.create_student(aluno, password)

        return aluno


# class AlunoLoginSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Aluno
#         fields = ('username', 'password')



class ServidorSerializer(serializers.ModelSerializer):
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
        # fields = ServidorSerializer.Meta.fields + ('formacao', 'id_tipo',)
        fields = _PessoaSerializer.Meta.fields + ('formacao', 'id_tipo',)

    def create(self, validated_data):
        professor = ServidorSerializer.create(self, validated_data, True)
        return professor


# class ProfessorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Professor
#         fields = ('username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto',
#                   'formacao', 'id_tipo')


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
        fields = ('titulo', 'cor',)
