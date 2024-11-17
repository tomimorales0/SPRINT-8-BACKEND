from django.views.generic.detail import DetailView
from .models import Cliente


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/cliente_detail.html'
    context_object_name = 'cliente'
