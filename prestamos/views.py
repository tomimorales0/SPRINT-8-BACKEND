from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Prestamo, Cliente
from .forms import PrestamoForm

@login_required
def solicitar_prestamo(request):
    cliente = Cliente.objects.get(user=request.user)
    if request.method == 'POST':
        form = PrestamoForm(request.POST, initial={'cliente': cliente})
        if form.is_valid():
            prestamo = form.save(commit=False)
            prestamo.cliente = cliente
            prestamo.aprobado = True  # Approve automatically
            prestamo.save()

            # Actualizar saldo del cliente
            cliente.saldo += prestamo.monto
            cliente.save()

            return JsonResponse({'status': 'success', 'message': 'Solicitud aprobada'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = PrestamoForm(initial={'cliente': cliente})
    return render(request, 'prestamos/solicitar_prestamo.html', {'form': form})
