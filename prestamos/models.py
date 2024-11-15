from django.db import models
from clientes.models import Cliente

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    plazo = models.PositiveIntegerField(help_text="Plazo en meses")
    fecha_inicio = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Préstamo de {self.monto} para {self.cliente}"

    class Meta:
        db_table = 'Prestamos'
        verbose_name = 'Prestamo'
        verbose_name_plural = 'Prestamos'