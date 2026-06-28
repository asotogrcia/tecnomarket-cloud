from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    stock = models.PositiveIntegerField()
    imagen_url = models.URLField(max_length=500 ,blank=True, null=True)

    def __str__(self):
        return self.nombre
