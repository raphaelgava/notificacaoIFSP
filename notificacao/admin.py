from django.contrib import admin


from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin

from .models import Aluno
from .models import Professor
from .models import Servidor
from .models import Curso
from .models import Disciplina
from .models import Instituto
from .models import Local
from .models import Notificacao
from .models import Oferecimento
from .models import Salaalunos
from .models import Salaprofessores
from .models import Tiponotificacao
from .models import Tipoformacao

# Register your models here.

from .forms import AlunoForm


# class PessoaAdmin(admin.ModelAdmin):
#     list_display = ('prontuario', 'first_name', 'last_name')
#     fieldsets = [
#         ('Pessoa', {'fields': ['prontuario', 'first_name', 'last_name', 'email', 'password', 'senha2', 'sexo', 'datanascimento',]}),
#         ('Usuário', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups']}),
#     ]
#
# class AlunoAdmin(UserAdmin):
#     form = AlunoForm
#     fieldsets = [
#         (None, {'fields': ['turma']}),
#     ] + PessoaAdmin.fieldsets
#     exclude = ['username']


# class UserCreationForm(forms.ModelForm):
#     """A form for creating new users. Includes all the required
#     fields, plus a repeated password."""
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
#
#     class Meta:
#         model = Aluno
#         fields = ('email', 'first_name')
#
#     def clean_password2(self):
#         # Check that the two password entries match
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise forms.ValidationError("Passwords don't match")
#         return password2
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user
#
#
# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()
#
#     class Meta:
#         model = Aluno
#         fields = ('prontuario', 'email', 'password', 'first_name', 'is_active')
#
#     def clean_password(self):
#         # Regardless of what the user provides, return the initial value.
#         # This is done here, rather than on the field, because the
#         # field does not have access to the initial value
#         return self.initial["password"]
#
#
# class UserAdmin(BaseUserAdmin):
#     # The forms to add and change user instances
#     form = UserChangeForm
#     add_form = UserCreationForm
#
#     # The fields to be used in displaying the User model.
#     # These override the definitions on the base UserAdmin
#     # that reference specific fields on auth.User.
#     list_display = ('first_name', 'last_name')
#     fieldsets = [
#                     (None, {'fields': ['turma']}),
#                     ('Pessoa', {'fields': ['sexo', 'datanascimento',]}),
#                     ('Usuário', {'fields': ['is_staff', 'is_active', 'is_superuser', 'groups']})
#                 ]
#     # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
#     # overrides get_fieldsets to use this attribute when creating a user.
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'password1', 'password2', 'prontuario')}
#          ),
#     )
#     search_fields = ('prontuario',)
#     ordering = ('prontuario',)
#     filter_horizontal = ()




admin.site.register(Aluno, UserAdmin)
# admin.site.register(Aluno)
admin.site.register(Professor, UserAdmin)
admin.site.register(Servidor, UserAdmin)
admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(Instituto)
admin.site.register(Local)
admin.site.register(Notificacao)
admin.site.register(Oferecimento)
admin.site.register(Salaalunos)
admin.site.register(Salaprofessores)
admin.site.register(Tiponotificacao)
admin.site.register(Tipoformacao)