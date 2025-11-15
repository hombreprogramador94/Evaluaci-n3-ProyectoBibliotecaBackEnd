from django.contrib import admin
from .models import Sala, Reserva #Importamos los modelos creados. 

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    #Esto mostrará estás columnas en la lista de salas:
    list_display = ('nombre', 'capacidad', 'habilitada')
    #Esto agrega un filtro al costado de "Habilitada"
    list_filter = ('habilitada',)
    #Esto agrega una barra de búsqueda en base al nombre
    search_fields=('nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    #Mostraremos la sala, el rut y las horas. 
    list_display = ('sala','rut_persona','hora_inicio','hora_termino')
    #Filtro por sala
    list_filter = ('sala',)
    #Agrega barra de busqueda por rut
    search_fields = ('rut_persona',)

