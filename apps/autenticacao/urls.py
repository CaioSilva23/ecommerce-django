from django.urls import path
from . import views


app_name = 'autenticacao'

urlpatterns = [
    path('autenticacao/', views.Autenticacao.as_view(), name='autenticacao'),
    path('login/', views.Login.as_view(), name='login'),
    path('cadastro/', views.Cadastro.as_view(), name='cadastro'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),
    path('endereco/', views.Endereco.as_view(), name='endereco'),
]
