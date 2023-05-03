from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import EnderecoForm, RegisterForms, UpdateForms
from django.contrib.auth import login
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .models import Endereco
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# class Login(LoginView):
# def post(self, *args, **kwargs):
#     form = LoginForm(self.request.POST)
#     username = self.request.POST.get('username')
#     password = self.request.POST.get('password')
#     if form.is_valid():
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(self.request, user)
#             return redirect(reverse('produto:list'))
#         else:
#             messages.error(self.request, 'Usuário ou senha inválido')
#     else:
#         messages.error(self.request, 'Credenciais inválidas')

#     return redirect(reverse('autenticacao:login'))

# def get(self, *args, **kwargs):
#     if not self.request.user.is_authenticated:
#         form = LoginForm()
#         return render(self.request, 'login.html', {"form": form})
#     else:
#         return redirect(reverse('produto:list'))


class Cadastro(CreateView):
    form_class = RegisterForms
    template_name = 'register.html'
    success_url = reverse_lazy('autenticacao:login')

    def form_valid(self, form):
        messages.success(self.request, 'Cadastro realizado com sucesso!')
        return super().form_valid(form)
    # def get(self, *args, **kwargs):
    #     if not self.request.user.is_authenticated:
    #         form = RegisterForm()
    #         return render(self.request, 'register.html', {"form": form})
    #     else:
    #         return redirect(reverse('produto:list'))

    # def post(self, *args, **kwargs):
    #     form = RegisterForm(self.request.POST)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.set_password(user.password)
    #         user.save()
    #         messages.success(self.request, 'Cadastro realizado com sucesso.')
    #         return redirect(reverse('autenticacao:login'))
    #     else:
    #         return render(self.request, 'register.html', {'form': form})


class UpdatePerfil(LoginRequiredMixin, UpdateView):
    template_name = 'perfil.html'
    model = User
    form_class = UpdateForms

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save(commit=False)
        login(self.request, user=user)
        messages.success(self.request, 'Perfil editado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('autenticacao:update_perfil', kwargs={'pk': self.get_object().pk})

    # def get(self, *args, **kwargs):
    #     user = self.request.user
    #     form = PerfilForm(instance=user)
    #     return render(self.request, 'perfil.html', {'form': form})

    # # UPDATE PERFIL DE USUÁRIO
    # def post(self, *args, **kwargs):
    #     form = PerfilForm(data=self.request.POST, instance=self.request.user)
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         user.set_password(user.password)
    #         user.save()
    #         login(self.request, user=user)
    #         messages.success(self.request, 'Perfil editado com sucesso')
    #         return redirect(reverse('autenticacao:perfil'))
    #     else:
    #         messages.error(self.request, 'Erro ao editar o perfil')
    #         return render(self.request, 'perfil.html', {'form': form})


class EnderecoList(LoginRequiredMixin, ListView):
    template_name = 'endereco.html'
    model = Endereco
    context_object_name = 'enderecos'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx['enderecos'] = Endereco.objects.filter(user=self.request.user)
        return ctx
    # def get(self, *args, **kwargs):
    #     enderecos = EnderecoModel.objects.filter(user=self.request.user)
    #     return render(self.request, 'endereco.html', {'enderecos': enderecos})


class UpdateEndereco(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        endereco = get_object_or_404(Endereco, id=kwargs['pk'])
        form = EnderecoForm(instance=endereco)
        return render(self.request, 'form_endereco.html', {'form':form})

    def post(self, *args, **kwargs):
        endereco = get_object_or_404(Endereco, id=kwargs['pk'])
        form = EnderecoForm(self.request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(self.request, 'Endereço atualizado com sucesso.')
            return redirect(reverse('autenticacao:endereco'))
        else:
            messages.error(self.request, 'Erro ao atualizar o seu endereço')
            return render(self.request, 'form_endereco.html', {'form': form})


class NovoEndereco(LoginRequiredMixin, View):
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


class DeleteEndereco(LoginRequiredMixin, DeleteView):
    model = Endereco
    success_url = reverse_lazy('autenticacao:endereco')

    def get_success_url(self) -> str:
        messages.success(self.request, 'Endereço deletado com sucesso!')
        return super().get_success_url()
    # def get(self, *args, **kwargs):
    #     endereco = get_object_or_404(Endereco, id=kwargs['pk'])
    #     endereco.delete()
    #     return redirect(reverse('autenticacao:endereco'))
