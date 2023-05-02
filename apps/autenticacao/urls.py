from django.urls import path
from . import views


app_name = 'autenticacao'

urlpatterns = [
    # path('autenticacao/', views.Autenticacao.as_view(), name='autenticacao'),
    path('login/', views.Login.as_view(), name='login'),
    path('cadastro/', views.Cadastro.as_view(), name='cadastro'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('perfil/', views.Perfil.as_view(), name='perfil'),


    path('endereco/', views.EnderecoList.as_view(), name='endereco'),
    path('novo_endereco/', views.NovoEndereco.as_view(), name='novo_endereco'),
    path('delete_endereco/<int:pk>/', views.DeleteEndereco.as_view(), name='delete_endereco'),
    path('update_endereco/<int:pk>/', views.UpdateEndereco.as_view(), name='update_endereco'),
]
