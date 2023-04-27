from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    # pedido/
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('finalizar/', views.Finalizar.as_view(), name='finalizar'),
    path('detalhes/', views.Detalhes.as_view(), name='detalhes'),
]
