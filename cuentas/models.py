from django.db import models
from clientes.models import Cliente

class Cuenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    numero_cuenta = models.CharField(max_length=20, unique=True)
    tipo = models.CharField(max_length=50)
    saldo = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Cuenta - {self.cliente}"

    class Meta:
        db_table = 'Cuentas'
        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'