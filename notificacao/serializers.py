from rest_framework import serializers

from .models import Aluno
from .models import Servidor
from .models import Professor
from .models import Notificacao
from .models import Tipoformacao
from .models import Tiponotificacao

class AlunoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Aluno
		fields = ('prontuario', 'nome', 'senha', 'sexo', 'datanascimento', 'email', 'ativo', 'id_instituto', 'turma',)


class ServidorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Servidor
		fields = ('prontuario', 'nome', 'senha', 'sexo', 'datanascimento', 'email', 'ativo', 'id_instituto', 'funcao',)


class ProfessorSerializer(serializers.ModelSerializer):
	class Meta:
		model = Professor
		fields = ('prontuario', 'nome', 'senha', 'sexo', 'datanascimento', 'email', 'ativo', 'id_instituto', 'formacao', 'id_tipo')


class NotificacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Notificacao
		fields = ('datahora', 'id_tipo', 'id_local', 'descricao', 'titulo', 'prontuario', 'remetente')


class TipoFormacaoSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tipoformacao
		fields = ('id','descricao',)


class TipoNotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
	    model = Tiponotificacao
	    fields = ('id','titulo','cor',)


