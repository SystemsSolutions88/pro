from django import forms
from .models import Competidor

class CompetidorForm(forms.ModelForm):
    class Meta:
        model = Competidor
        fields = ['nombre', 'edad', 'equipo', 'tipo_sangre', 'alergia', 'pista', 'categoria']
        widgets = {
            'tipo_sangre': forms.Select(choices=Competidor.TIPOS_SANGRE),
            'pista': forms.Select(choices=Competidor.PISTAS),
            'categoria': forms.Select(choices=Competidor.CATEGORIAS),
        }
