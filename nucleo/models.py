from django.db import models
from django.utils import timezone #Necesario para poder manejar fechas y horas.



#MODELOS


#Modelo sala:
class Sala(models.Model):
    """
    Modelo para representar una Sala de estudio. 
    """
    #Requisito: "Nombre de la sala" 
    nombre = models.CharField(max_length=100)
    #Requisito: "Capacidad máxima"
    capacidad = models.IntegerField()
    #Requisito: Queremos que el administrador pueda habilitar una sala.
    habilitada = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (Cap: {self.capacidad})" #Forma de visualizar con formato el admin. 



    @property
    def disponibilidad(self):
        """
        Parte importante de la logica.
        No guardamos la disponibilidad en la BD, la CALCULAMOS.
        Así cumplimos que la sala "Se considera libre automaticamente. 
        """

        #1- Obtenemos la hora actual. 
        ahora = timezone.now()
        #2.- Buscamos si existe alguna reserva ACTIVA para la sala.
        # - Que empiece ANTES de ahora.
        # - Que termine DESPUÉS de ahora. 
        reserva_activa = Reserva.objects.filter(
            sala=self,
            hora_inicio__lte=ahora, #Menor o Igual (Empezó antes o justo ahora. )
            hora_termino__gte=ahora #Mayor o Iugal (Termina después o justo ahora. )
        ).exists() # .exists() Devuelve True si encuentra una, False sino. 
        #3.- Una sala está disponible sí:_
        # No hay una reserva activa
        # Está habilitada por un admin. 
        if not reserva_activa and self.habilitada:
            return "Disponible" #Requisito.
        else:
            return "Reservada"
        


class Reserva(models.Model):
    """
    Modelo para representar una Reserva de una Sala.
    """

    #Requisito: Rut de la persona que reserva
    rut_persona = models.CharField(max_length=12)
    #Requisito: "Fecha y Hora de inicio. (Se crea automaticamente)"
    #auto_now_add=True pone la fecha/hora actual al crear el registro.
    hora_inicio = models.DateTimeField(auto_now_add=True)
    #BLANK= True y null=True, es temporal, lo calcularemos despues
    hora_termino = models.DateTimeField(editable=False)
    # models.CASCADE Significa que si se borra la sala, se borran las reservas también.
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva de {self.sala.nombre} por {self.rut_persona}"
    
    def save(self, *args, **kwargs):
        """
        Sobreescribimos el método save() para calcular la hora de termino. 
        """
        #Requisito : Pide solo dos 2 horas por defecto y máximo. 
        if not self.id: #Solo al crear la reserva
            #Si hora_inicio ya está (Como con auto_now_add,), se utiliza.
            if self.hora_inicio:
                self.hora_termino = self.hora_inicio + timezone.timedelta(hours=2)
            else:
                #Si no, por si acaso, usa timezone.now()
                self.hora_inicio = timezone.now()
                self.hora_termino = self.hora_inicio+ timezone.timedelta(hours=2)

        super(Reserva,self).save(*args,**kwargs)# Llama al método save original.
