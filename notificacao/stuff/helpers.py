from django.contrib.auth.models import Group

from notificacao.stuff.constants import GroupConst, PersonConst


class CreatePerson:
    def create_student(self, password):
        if self is not None:
            if password is not None:
                self.set_password(password)
                if not Group.objects.filter(name=GroupConst.STUDENT).exists():
                    Group.objects.create(name=GroupConst.STUDENT)
                self.groups.add(Group.objects.get(name=GroupConst.STUDENT))
                self.save()

        return self

    def create_employee(self, password, professor):
        if self is not None:
            if password is not None:
                self.set_password(password)
                if not Group.objects.filter(name=GroupConst.EMPLOYEE).exists():
                    Group.objects.create(name=GroupConst.EMPLOYEE)
                if self.admin == True:
                    self.groups.add(Group.objects.get(name=GroupConst.ADMIN))
                else:
                    if professor == True:
                        self.funcao = 'Professor'
                        self.groups.add(Group.objects.get(name=GroupConst.PROFESSOR))
                    else:
                        self.groups.add(Group.objects.get(name=GroupConst.EMPLOYEE))
                self.save()

        return self

    def update_password(self, password):
        if self is not None:
            if password is not None:
                if len(password) >= PersonConst.PASSWORD_LENGTH:
                    self.set_password(password)
                    self.save()

        return self
