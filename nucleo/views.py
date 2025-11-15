from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Sala, Reserva
# Importamos el formulario.
from .forms import ReservaForm

# Create your views here.

def lista_salas(request):
    """
    Vista para la página principal.
    Muestra todas las salas y la disponibilidad.
    """
    # 1.- Obtenemos todas las salas de la BD.
    salas = Sala.objects.all()
    # 2.- Preparamos el contexto para la plantilla.
    context = {
        'lista_de_salas': salas,
    }    

    # 3.- Renderizamos (Se dibuja) la plantilla HTML.
    return render(request, 'nucleo/lista_salas.html', context)

def detalle_sala(request, sala_id):
    """
    Vista para la página de detalle de una sala.
    Muestra la info de la sala y los detalles de la reserva si existe. 
    """
    # 1.- Obtenemos la sala especifica, o mostramos error 404 si no existe.
    sala = get_object_or_404(Sala, id=sala_id)
    
    # 2.- Verificamos si la sala esta reservada.
    reserva_activa = None
    if sala.disponibilidad == 'Reservada':
        #Si esta reservada, buscaremos la reserva activa. 
        ahora = timezone.now()
        reserva_activa = Reserva.objects.filter(
            sala = sala,
            hora_inicio__lte =ahora,
            hora_termino__gte=ahora
        ).first() #.first() Nos da el objeto de la reserva, no solo True/False.

    # 3.- Preparamos el contexto
    context = {
        'sala': sala,
        'reserva': reserva_activa,
    }
    
    # 4.- Renderizamos la plantilla
    return render(request, 'nucleo/detalle_sala.html', context)

#-- Vista de reserva --


def crear_reserva(request, sala_id):
    """    
    Vista para crear una reserva usando un ModelForm.
    """
    sala = get_object_or_404(Sala, id=sala_id)

    if request.method == 'POST':
        #Si el usuario envio el formulario
        form = ReservaForm(request.POST)
        if form.is_valid():
            #El formulario es valido, pero no se guarda aun.
            reserva = form.save(commit=False)
            reserva.sala = sala #Asignamos la sala correcta.
            #La hora_inicio y hora_termino se calculan solas en models.py
            reserva.save() #Ahora sí guardamos.
            # Redirigimos a la pagina de detalle
            return redirect('nucleo:detalle_sala', sala_id=sala.id)
    else:
        #Si el usuario acaba de entrar (GET)
        form = ReservaForm()

    context = {
            'form': form,
            'sala': sala,
    }
    return render(request, 'nucleo/crear_reserva.html', context)
