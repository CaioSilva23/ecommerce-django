from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from .forms import RegisterForm, LoginForm, EnderecoForm,PerfilForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib import messages
from .models import Endereco as EnderecoModel
from django.contrib.auth.mixins import LoginRequiredMixin


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

        return redirect(reverse('autenticacao:login'))

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = LoginForm()
            return render(self.request, 'login.html', {"form": form})
        else:
            return redirect(reverse('produto:list'))


class Cadastro(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            form = RegisterForm()
            return render(self.request, 'register.html', {"form": form})
        else:
            return redirect(reverse('produto:list'))

    def post(self, *args, **kwargs):
        form = RegisterForm(self.request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(self.request, 'Cadastro realizado com sucesso.')
            return redirect(reverse('autenticacao:login'))
        else:
            return render(self.request, 'register.html', {'form': form})


class Logout(View):
    def get(self, *args, **kwargs):
        messages.success(self.request, 'Logout sucedido')
        logout(self.request)
        return redirect(reverse('autenticacao:login'))


class Perfil(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        form = PerfilForm(instance=user)
        return render(self.request, 'perfil.html', {'form': form})

    # UPDATE PERFIL DE USUÁRIO
    def post(self, *args, **kwargs):
        form = PerfilForm(data=self.request.POST, instance=self.request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(self.request, user=user)
            messages.success(self.request, 'Perfil editado com sucesso')
            return redirect(reverse('autenticacao:perfil'))
        else:
            messages.error(self.request, 'Erro ao editar o perfil')
            return render(self.request, 'perfil.html', {'form': form})


class EnderecoList(View):
    def get(self, *args, **kwargs):
        enderecos = EnderecoModel.objects.filter(user=self.request.user)
        return render(self.request, 'endereco.html', {'enderecos': enderecos})


class UpdateEndereco(View):
    def get(self, *args, **kwargs):
        endereco = get_object_or_404(EnderecoModel, id=kwargs['pk'])
        form = EnderecoForm(instance=endereco)
        return render(self.request, 'form_endereco.html', {'form':form})

    def post(self, *args, **kwargs):
        endereco = get_object_or_404(EnderecoModel, id=kwargs['pk'])
        form = EnderecoForm(self.request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Endereço atualizado com sucesso.')
            return redirect(reverse('autenticacao:endereco'))
        else:
            messages.error(self.request, 'Erro ao atualizar o seu endereço')
            return render(self.request, 'form_endereco.html', {'form': form})


class NovoEndereco(View):
    def get(self, *args, **kwargs):
        form = EnderecoForm()
        return render(self.request, 'form_endereco.html', {'form': form})

    def post(self, *args, **kwargs):
        form = EnderecoForm(self.request.POST)
        if form.is_valid():
            endereco = form.save(commit=False)
            endereco.user = self.request.user
            endereco.save()
            messages.success(self.request, 'Endereço salvo com sucesso.')
            return redirect(reverse('autenticacao:endereco'))
        else:
            messages.error(self.request, 'Dados inválidos')
            return render(self.request, 'form_endereco.html', {'form': form})


class DeleteEndereco(View):
    def get(self, *args, **kwargs):
        endereco = get_object_or_404(EnderecoModel, id=kwargs['pk'])
        endereco.delete()
        return redirect(reverse('autenticacao:endereco'))
