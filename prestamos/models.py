from django.db import models
from clientes.models import Cliente

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo_prestamo = models.CharField(max_length=100, null=False, default= 'Classic')
    fecha_inicio = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    aprobado = models.BooleanField(default=True)

    def __str__(self):
        return f"Préstamo de {self.cliente.user.username} - {self.monto}"