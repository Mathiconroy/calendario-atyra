from django.db import models

class Reservas(models.Model):
    ESTADOS = [
        (0, 'Pendiente'),
        (1, 'Ocupado'),
    ]
    TIPOS_ADELANTO = [
        (0, 'Giro'),
        (1, 'Depósito'),
        (2, 'Otro'),
    ]
    casa = models.IntegerField(null=False)
    nombre = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=True)
    cantidad_adultos = models.IntegerField(null=False)
    cantidad_menores = models.IntegerField(default=0)
    cantidad_gratis = models.IntegerField(default=0)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    notas = models.TextField()
    estado = models.IntegerField(default=1, choices=ESTADOS)
    tipo_adelanto = models.IntegerField(default=2, choices=TIPOS_ADELANTO)
    precio = models.CharField(default=0, max_length=50)

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Casa: {self.casa} {self.fecha_inicio.strftime('%d/%m/%Y')} - {self.fecha_fin.strftime('%d/%m/%Y')}"
