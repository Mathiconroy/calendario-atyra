from django.db import models

class Reservas(models.Model): # THE ID FIELD IS ADDED AUTOMATICALLY
    id = models.IntegerField(primary_key=True)
    casa = models.IntegerField(null=False)
    nombre = models.CharField(null=False, max_length=150)
    email = models.EmailField(null=True)
    cantidad_personas = models.IntegerField(null=False)
    fecha_inicio = models.DateField(null=False)
    fecha_fin = models.DateField(null=False)
    notas = models.TextField()

    def __str__(self):
        return self.nombre
