from django.db import models
from cuentas.models import Cuenta

class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_movimiento = models.CharField(max_length=50)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.cuenta}"

    class Meta:
        db_table = 'Movimientos'
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'