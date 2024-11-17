from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cuenta
from django.urls import reverse_lazy

class CuentaCreateView(LoginRequiredMixin, CreateView):
    model = Cuenta
    fields = ['cliente', 'tipo_cuenta',]
    template_name = 'cuentas/cuenta_form.html'
    success_url = reverse_lazy('cuentas_list')
