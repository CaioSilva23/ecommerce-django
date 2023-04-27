from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    # produto/

    path('', views.ListProduts.as_view(), name='list'),
    path('<slug:slug>', views.DetailProducts.as_view(), name='detail'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),

    # produto/add_carrinho
    path('add_carrinho/',
         views.AddAoCarrinho.as_view(),
         name='add_carrinho'),

    # limpar carrinho produto/limpar_carrinho
    path("limpar_carrinho/",
         views.LimparCarrinho.as_view(),
         name="limpar_carrinho"),


    # produto/remover_carrinho
    path('remove_carrinho/',
         views.RemoveDoCarrinho.as_view(),
         name='remove_carrinho'),
]
