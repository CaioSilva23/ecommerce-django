from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.contrib import messages






class Autenticacao(View):
    def get(self, *args, **kwargs):
        form = LoginForm()
        form_register = RegisterForm()
        ctx = {
            'form_register': form_register,
            'form': form

        }
        return render(self.request, 'login.html', context=ctx)

class Login(View):
    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        if form.is_valid():
            user = authenticate(username=username,password=password)
            if user is not None:
                login(self.request, user)
                return redirect(reverse('produto:list'))
            else:
                messages.error(self.request, 'Usuário ou senha inválido')
        else:
            messages.error(self.request, 'Credenciais inválidas')

        return redirect(reverse('autenticacao:autenticacao'))

    def get(self):
        raise Http404()

 


class Cadastro(View):
    pass


class Logout(View):
    def get(self, *args, **kwargs):
        messages.success(self.request, 'Logout sucedido')
        logout(self.request)
        return redirect(reverse('autenticacao:autenticacao'))