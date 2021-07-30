from django.db import models
import re  # el módulo regex


class UserManager(models.Manager):
    def validador_user(self, postData):
        errors = {}
        # REGEX VALIDADOR SOLO CARACTERES Y ESPACIOS
        CHAR_REGEX = re.compile(
            r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$')
        if len(postData['name']) < 3:
            errors['name'] = "Largo de nombre inválido! (al menos 3 caracteres de largo)"
        if len(postData['username']) < 3:
            errors['username'] = "Largo de username inválido! (al menos 3 caracteres de largo)"
        if not CHAR_REGEX.match(postData['name']):
            errors['name'] = "Nombre solo acepta caracteres alfabéticos sin espacios al comienzo"
        if len(postData['password']) < 8:
            errors['password'] = "Largo de password inválido!"
        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords no coincidentes!"
        return errors

# Create your models here.


class User (models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()  # LINEA QUE AGREGA EL MANAGER DE VALIDACION PARA USERS

    def __repr__(self):
        return f"< Id #({self.id}) Name: {self.name} Last name : {self.username}>"

    def __str__(self):
        return f"< Id #({self.id}) Name: {self.name} Last name : {self.username}>"
