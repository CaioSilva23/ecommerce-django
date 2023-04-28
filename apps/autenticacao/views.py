from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import RegisterForm, LoginForm, EnderecoForm
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from .models import Endereco as EnderecoModel


class Autenticacao(View):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse('produto:list'))
        else:
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
            user = authenticate(username=username, password=password)
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

    def post(self, *args, **kwargs):
        data = self.request.POST or None
        instance = None if not self.request.user.is_authenticated else self.request.user

        form_cadastro = RegisterForm(data=data, instance=instance)
        if form_cadastro.is_valid():
            user = form_cadastro.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(self.request, user=user)
            if not instance:
                messages.success(self.request, 'Cadastro realizado com sucesso.')
            else:
                messages.success(self.request, 'Perfil editado com sucesso')
                return redirect(reverse('autenticacao:perfil'))
            return redirect(reverse('produto:list'))
        else:
            form = LoginForm()
            messages.error(self.request, 'Dados inválidos!')
            return render(self.request, 'login.html', {"form_register": form_cadastro,'form': form})


class Logout(View):
    def get(self, *args, **kwargs):
        messages.success(self.request, 'Logout sucedido')
        logout(self.request)
        return redirect(reverse('autenticacao:autenticacao'))


class Perfil(View):
    def get(self, *args, **kwargs):
        user = self.request.user
        form = RegisterForm(instance=user)
        return render(self.request, 'perfil.html', {'form': form})


class Endereco(View):

    
    def get(self, *args, **kwargs):
        endereco = EnderecoModel.objects.get(user=self.request.user)
        form_endereco = EnderecoForm(instance=endereco)
        return render(self.request, 'endereco.html', {'form_endereco': form_endereco})
    
    def post(self, *args, **kwargs):
        endereco = EnderecoModel.objects.get(user=self.request.user)
        form_endereco = EnderecoForm(data=self.request.POST, instance=endereco)
        if form_endereco.is_valid():
            endereco = form_endereco.save(commit=False)
            endereco.user = self.request.user
            endereco.save()
            messages.success(self.request, 'Endereço editado com sucesso!')
        else:
            messages.error(self.request, 'Dados inválidos, tente novamente')
        return redirect(reverse('autenticacao:endereco'))

