from django.db import models
import re	# el módulo regex
from datetime import datetime, date

class UserManager(models.Manager):
    def validador_user(self, postData):
        errors = {}
        # REGEX VALIDADOR SOLO CARACTERES Y ESPACIOS
        CHAR_REGEX = re.compile(r'^[a-zA-ZÀ-ÿ\u00f1\u00d1]+(\s*[a-zA-ZÀ-ÿ\u00f1\u00d1]*)*[a-zA-ZÀ-ÿ\u00f1\u00d1]+$')
        if len(postData['name'])<3:
            errors['name'] = "Largo de nombre inválido! (al menos 3 caracteres de largo)"
        if len(postData['username'])<3:
            errors['username'] = "Largo de username inválido! (al menos 3 caracteres de largo)"
        if not CHAR_REGEX.match(postData['name']):
            errors['name'] = "Nombre solo acepta caracteres alfabéticos sin espacios al comienzo"
        if len(postData['password'])<8:
            errors['password'] = "Largo de password inválido!"
        if postData['password'] != postData['password_confirm']:
            errors['password'] = "Passwords no coincidentes!"
        return errors

class TravelManager(models.Manager):
    def validador_travel(self,postData):
        errors = {}
        now = datetime.now()
        # fec_datetime = datetime.strptime(postData['travel_date_from'], '%Y-%m-%d')
        # print(type(now))
        # print(type(fec_datetime))
        if len(postData['destination']) <6 :
            errors['destination'] = "El largo de destino debe ser mayor a 6 caracteres"
        if len(postData['description']) <6 :
            errors['description'] = "El largo de la descripción debe ser mayor a 6 caracteres"
        if postData['travel_date_from'] == "":
            errors['travel_date_from'] = "Error en fecha de inicio de viaje, no puede estar vacía"
        else :
            fecha_inicio_viaje = datetime.strptime(postData['travel_date_from'], '%Y-%m-%d').date()
            # OJO CON ESTA RUTINA QUE PERMITE VER EL TIPO DE OBJETO 
            # print(type(now))
            # print(type(fecha_inicio_viaje))
            # print(now)
            # print (fecha_inicio_viaje)
            if fecha_inicio_viaje < now.date() :
                errors['travel_date_from'] = "Fecha inicio del viaje no puede ser menor a la fecha actual."
        if postData['travel_date_to'] == "":
            errors['travel_date_to'] = "Error en fecha de término del viaje, no puede estar vacía"
        else :
            fecha_fin_viaje = datetime.strptime(postData['travel_date_to'], '%Y-%m-%d').date()
            if fecha_fin_viaje < now.date() or fecha_fin_viaje < fecha_inicio_viaje:
                errors['travel_date_to'] = "Fecha de término del viaje no puede ser menor a la fecha actual o menor a la fecha de inicio del viaje"
        return errors

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.TextField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager() #LINEA QUE AGREGA EL MANAGER DE VALIDACION PARA USERS
    def __repr__(self):
        return f"< Id #({self.id}) Name: {self.name} Last name : {self.username}>"
    def __str__(self):
        return f"< Id #({self.id}) Name: {self.name} Last name : {self.username}>"


class Travel (models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    usuario = models.ForeignKey(User, related_name='travels', on_delete=models.CASCADE)
    travelers = models.ManyToManyField(User, related_name='traveler')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TravelManager() #LINEA QUE AGREGA EL MANAGER DE VALIDACION PARA VIAJES
    def __repr__(self):
        return f"< Id #({self.id}) Destination: {self.destination} Description : {self.description}>"
    def __str__(self):
        return f"< Id #({self.id}) Destination: {self.destination} Description : {self.description}>"
