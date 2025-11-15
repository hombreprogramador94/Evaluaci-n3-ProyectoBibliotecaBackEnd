from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    """
    Este es el ModelForm que pide el requisito
    """

    class Meta:
        #1.- Le decimos en qué modelo se basa.
        model = Reserva

        #2.- Le decimos qué campos del modelo mostraremos.
        # Solo usaremos URT, porqué la sala la asigna la vista y las horas se calculan solas.
        fields = ['rut_persona']
        
        #3.- Le ponemos una etiqueta
        labels = {
            'rut_persona': 'Ingrese su RUT (con guión)',
        }