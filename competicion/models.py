from django.db import models
from django.utils import timezone

class Competidor(models.Model):
    TIPOS_SANGRE = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    PISTAS = [
        ('Larga', 'Pista Larga'),
        ('Corta', 'Pista Corta'),
    ]

    CATEGORIAS = [(chr(i), chr(i)) for i in range(65, 91)]  # Genera categorías de 'A' a 'Z'

    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    equipo = models.CharField(max_length=100)
    tipo_sangre = models.CharField(max_length=3, choices=TIPOS_SANGRE, default='A+')
    alergia = models.CharField(max_length=10)
    pista = models.CharField(max_length=10, choices=PISTAS, default='Larga')
    categoria = models.CharField(max_length=1, choices=CATEGORIAS, default='A')
    tiempo_inicio = models.DateTimeField(null=True, blank=True)
    tiempo_fin = models.DateTimeField(null=True, blank=True)
    numero_corredor = models.IntegerField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.numero_corredor is None:
            max_numero = Competidor.objects.aggregate(models.Max('numero_corredor'))['numero_corredor__max']
            self.numero_corredor = (max_numero or 0) + 1
        super().save(*args, **kwargs)

    def iniciar_cronometro(self):
        self.tiempo_inicio = timezone.now()

    def detener_cronometro(self):
        self.tiempo_fin = timezone.now()

    def obtener_tiempo(self):
        if self.tiempo_inicio and self.tiempo_fin:
            return (self.tiempo_fin - self.tiempo_inicio).total_seconds()
        return None

    def __str__(self):
        return f'Corredor {self.numero_corredor}: {self.nombre}'

class Resultado(models.Model):
    competidor = models.ForeignKey(Competidor, on_delete=models.CASCADE)
    tiempo_total = models.DecimalField(max_digits=10, decimal_places=2)
    posicion = models.IntegerField()

    def __str__(self):
        return f'Resultado de {self.competidor.nombre} - Posición: {self.posicion}'
