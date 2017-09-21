from rest_framework import serializers

from .models import Aluno
from .models import Instituto
from .models import Notificacao
from .models import Oferecimento
from .models import Pessoa
from .models import Professor
from .models import Remetente
from .models import Servidor
from .models import TipoNotificacao
from .stuff.helpers import CreatePerson


class _PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        abstract = True
        # fields = ('pk','username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto',)
        # esta enviando também o password na busca, porém para fazer update da senha o campo password deve estar declarado!
        fields = (
        'pk', 'username', 'first_name', 'last_name', 'email', 'sexo', 'datanascimento', 'id_instituto', 'password',)


class AlunoSerializer(_PessoaSerializer):
    class Meta:
        model = Aluno
        fields = _PessoaSerializer.Meta.fields + ('turma',)

    def create(self, validated_data):
        aluno = serializers.ModelSerializer.create(self, validated_data)
        password = validated_data['password']
        aluno = CreatePerson.create_student(aluno, password)

        return aluno

    def update(self, instance, validated_data):
        aluno = serializers.ModelSerializer.update(self, instance, validated_data)
        password = validated_data['password']
        aluno = CreatePerson.update_password(aluno, password)

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

    def update(self, instance, validated_data):
        servidor = serializers.ModelSerializer.update(self, instance, validated_data)
        password = validated_data['password']
        servidor = CreatePerson.update_password(servidor, password)

        return servidor


class ProfessorSerializer(ServidorSerializer):
    class Meta:
        model = Professor
        fields = _PessoaSerializer.Meta.fields + ('formacao', 'tipo_formacao',)

    def create(self, validated_data):
        professor = ServidorSerializer.create(self, validated_data, True)
        return professor

    def update(self, instance, validated_data):
        professor = serializers.ModelSerializer.update(self, instance, validated_data)
        password = validated_data['password']
        professor = CreatePerson.update_password(professor, password)

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
