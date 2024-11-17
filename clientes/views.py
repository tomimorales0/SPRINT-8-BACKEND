from django.views.generic.detail import DetailView
from .models import Cliente
from django.contrib.auth.mixins import LoginRequiredMixin


class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
