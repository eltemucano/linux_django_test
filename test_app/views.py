from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import request
from .models import User
import bcrypt

# Create your views here.


def index(request):

    return render(request, 'index.html')


def login(request):
    if request.method == "POST":
        user = User.objects.filter(username=request.POST['username'])
        if user:
            log_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), log_user.password.encode()):
                user_logged = {
                    "id": log_user.id,
                    "name": log_user.name,
                    "username": log_user.username
                }
                request.session['usuario'] = user_logged
                messages.success(
                    request, f"Bienvenido al sitio usuario : {user_logged['username']}")
                print(request.session['usuario'])
                return redirect('/travels')
            else:
                messages.error(request, "Password o Email incorrectos.")
        else:
            messages.error(request, "Password o Email incorrectos.")
    return redirect("/")


def logout(request):
    # Acá va el procedimiento de detección del usuario y eliminación de su key de session
    request.session.flush()  # Prueba Nº1 Test
    messages.success(request, 'Usuario se ha deslogueado...')
    return redirect('/')


def register(request):
    if request.method == "POST":
        # Cargo valores de campo/sesion para devolver a formulario en caso de error
        request.session['registro_name'] = request.POST['name']
        request.session['registro_username'] = request.POST['username']
        # verifico errores existentes
        errors = User.objects.validador_user(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        verifica_username = request.POST['username']
        username_registrado = User.objects.filter(username=verifica_username)
        if username_registrado:
            messages.error(
                request, "ERROR: Este nombre de usuario ya está registrado.")
            return redirect('/register')
        # PROBANDO ESTAS INSTRUCCIONES
        # Vaciado valores de campo/sesion
        request.session['registro_name'] = ""
        request.session['registro_username'] = ""
        #  creo el hash de la password debidamente encriptada
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        # creo el proceso de save para el registro
        new_user = User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            password=pw_hash
        )
        # del objeto validado anteriormente y grabado, tomo los campos necesarios para
        # utilizarlos en una nueva sesion
        request.session['usuario'] = {
            "id": new_user.id,
            "name": new_user.name,
            "user_alias": new_user.username,
        }
        messages.success(request, f"Bienvenido a nuestra aplicación")
        return redirect('/')
    return render(request, 'register.html')
