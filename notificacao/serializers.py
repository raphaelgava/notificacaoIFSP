from rest_framework import serializers

from .models import Aluno
from .models import Notificacao
from .models import Pessoa
from .models import Professor
from .models import Servidor
from .models import Tipoformacao
from .models import Tiponotificacao
from .stuff.helpers import CreatePerson


#
# class AlunoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Aluno
#         fields = (
#         'username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto', 'turma')
#
#     def create(self, validated_data):
#         aluno = serializers.ModelSerializer.create(self, validated_data)
#         password = validated_data['password']
#         # if aluno is not None:
#         # aluno.set_password(validated_data['password'])
#         # if not Group.objects.filter(name='Aluno').exists():
#         # 	group = Group.objects.create(name='Aluno')
#         # aluno.groups.add(Group.objects.get(name='Aluno'))
#         # aluno.save()
#         aluno = CreatePerson.create_student(aluno, password)
#
#         return aluno

# If you need the list of users that are in a group, you can do this instead:
#
# from django.contrib.auth.models import Group
# users_in_group = Group.objects.get(name="group name").user_set.all()



# aluno = Aluno.objects.create(
# 	username=validated_data['username'],
# 	first_name=validated_data['first_name'],
# 	last_name=validated_data['last_name'],
# 	email=validated_data['email'],
# 	sexo=validated_data['sexo'],
# 	datanascimento=validated_data['datanascimento'],
# 	id_instituto=validated_data['id_instituto'],
# 	turma=validated_data['turma']
# )
# aluno.set_password(validated_data['password'])
# aluno.save()

# return aluno


#
# class ServidorSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Servidor
# 		fields = ('username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto', 'funcao')


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


class AlunoLoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aluno
        fields = ('username', 'password')


class ServidorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servidor
        fields = _PessoaSerializer.Meta.fields + ('funcao',)

    def create(self, validated_data):
        servidor = serializers.ModelSerializer.create(self, validated_data)
        password = validated_data['password']
        servidor = CreatePerson.create_employee(servidor, password)

        return servidor


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'sexo', 'datanascimento', 'id_instituto',
                  'formacao', 'id_tipo')


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacao
        fields = ('datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'username', 'remetente')


class TipoFormacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tipoformacao
        fields = ('id', 'descricao',)


class TipoNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tiponotificacao
        fields = ('id', 'titulo', 'cor',)
