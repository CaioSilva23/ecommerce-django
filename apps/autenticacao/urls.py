from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'autenticacao'

urlpatterns = [
    path('autenticacao/', views.Autenticacao.as_view(), name='autenticacao'),
    path('login/', views.Login.as_view(), name='login'),
    #path('cadastro/', auth_view.as_view(), name='cadastro'),
    path('logout/', views.Logout.as_view(), name='logout'),
]
