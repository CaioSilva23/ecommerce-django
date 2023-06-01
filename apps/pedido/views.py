from typing import Any
from django.views.generic import View, ListView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from produto.models import Variacao
from django.contrib import messages
from .models import Pedido, ItemPedido
from django.http import HttpRequest, HttpResponse, Http404
from django.urls import reverse


class Pagar(LoginRequiredMixin, DetailView):
    template_name = 'pagar.html'
    model = Pedido
    context_object_name = 'pedido'
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self.get_object().usuario.pk != self.request.user.pk:
            raise Http404
        return super().get(request, *args, **kwargs)

#TODO: verificar endereco e dados pessoais de salvar o pedido

class SalvarPedido(View):
    def get(self, *args, **kwargs):

        carrinho = self.request.session.get('carrinho')
        if not carrinho:
            return redirect('/')

        carrinho_ids = [i for i in carrinho]

        bd_variacoes = list(Variacao.objects.select_related('produto').filter(id__in=carrinho_ids))

        for variacao in bd_variacoes:
            id = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[id]['quantidade']
            preco_unit = carrinho[id]['preco_unitario_promo']

            if estoque < qtd_carrinho:
                carrinho[id]['quantidade'] = estoque
                carrinho[id]['preco_quantitativo_promo'] = estoque * preco_unit
                self.request.session.save()
                messages.info(self.request, 'Atenção, itens insuficiente no estoque, quantidades readequadas.')
                return redirect('produto:carrinho')



        qtd_carrinho = len(carrinho)
        valor_total = sum(i['preco_quantitativo_promo'] for i in carrinho.values())

        pedido = Pedido(
            usuario = self.request.user,
            total = valor_total,
            qtd_total = qtd_carrinho,
            status='C',
        )
        pedido.save()

        ItemPedido.objects.bulk_create(
            [ItemPedido(
                    pedido=pedido,
                    produto=v["produto_nome"],
                    produto_id=v["produto_id"],
                    varicao=v["variacao_nome"],
                    varicao_id=v["id_variacao"],
                    preco=v["preco_unitario_promo"],
                    quantidade=v["quantidade"],
                    imagem=v['imagem']
                    ) 
                for v in carrinho.values()]
        )

        del self.request.session['carrinho']
        return redirect(reverse('pedido:pagar', kwargs={'pk': pedido.pk}))


class ListarPedidos(ListView):
    template_name = 'listar.html'
    model = Pedido


class Finalizar(View):
    pass


class Detalhes(View):
    pass
