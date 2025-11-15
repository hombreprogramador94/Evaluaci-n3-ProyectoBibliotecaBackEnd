from django.urls import path
from . import views #Importa las vistas de la app Nucleo. 

#Esto es para darle un "Nombre" a este archivo de URLS.
#Nos permite usar el 'nucleo:lista_salas' en las plantillas
app_name = 'nucleo'

urlpatterns = [
    # URL: / (Pagina principal)
    # Vista: views.lista_salas
    # Nombre: 'lista_salas'
    path('', views.lista_salas, name='lista_salas'),

    # URL: /sala/1/ o (/sala/2/, etc. )
    # Vista: views.detalle_sala
    # Nombre: 'detalle_sala'
    path('sala/<int:sala_id>', views.detalle_sala, name='detalle_sala'),

    # URL para la reserva
    path('sala/<int:sala_id>/reservar/', views.crear_reserva, name='crear_reserva'),
]
