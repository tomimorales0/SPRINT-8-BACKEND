from django.db import models
from clientes.models import Cliente

class Tarjeta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    cvv_numero = models.CharField(max_length=4, unique=True)
    numero_tarjeta = models.CharField(max_length=16, unique=True)
    tipo_tarjeta = models.CharField(max_length=50)
    fecha_expiracion = models.DateField()


    def __str__(self):
        return f"Tarjeta {self.numero_tarjeta} -{self.tipo_tarjeta}- {self.cliente}"

    class Meta:
        db_table = 'Tarjetas'
        verbose_name = 'Tarjeta'
        verbose_name_plural = 'Tarjetas'