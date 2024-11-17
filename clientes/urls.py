from django.urls import path
from .views import ClienteDetailView

urlpatterns = [
    path("<int:pk>/", ClienteDetailView.as_view(), name='cliente_detail.html'),
]
