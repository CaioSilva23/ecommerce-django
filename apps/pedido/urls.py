from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    # pedido/
    path('pagar/<int:pk>/', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('listar/', views.ListarPedidos.as_view(), name='listar'),

    path('detalhes/', views.Detalhes.as_view(), name='detalhes'),
]
