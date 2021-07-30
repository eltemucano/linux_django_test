from django.urls import path, include
from . import views


# En esta sección defines las redirecciones a la vista
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),

]
