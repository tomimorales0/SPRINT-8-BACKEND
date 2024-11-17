# Generated by Django 5.1.3 on 2024-11-15 20:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cuenta', models.CharField(max_length=20, unique=True)),
                ('tipo_cuenta', models.CharField(max_length=50)),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=12)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
            ],
            options={
                'verbose_name': 'Cuenta',
                'verbose_name_plural': 'Cuentas',
                'db_table': 'Cuentas',
            },
        ),
    ]
