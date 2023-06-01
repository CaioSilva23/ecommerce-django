from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView
from django.views import View
from produto.models import Produto, Variacao, Categoria
from django.contrib import messages
from django.urls import reverse
from autenticacao.models import Endereco

# from pprint import pprint


class ListProduts(ListView):
    model = Produto
    template_name = 'produto/index.html'
    context_object_name = 'produtos'
    paginate_by = 8

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.select_related('categoria')
        qs = qs.order_by('nome').filter(publicado=True)
        return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx.update({"categorias": Categoria.objects.all()})

        nome = self.request.GET.get('nome')
        if nome:
            produtos = Produto.objects.filter(nome__icontains=nome)
            ctx['produtos'] = produtos
        return ctx


class CategoriaFiltro(ListProduts):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(categoria_id=self.kwargs['pk'])
        return qs


class CategoriaFiltroLancamento(ListProduts):
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(lancamento=True)
        return qs


class DetailProducts(DetailView):
    model = Produto
    template_name = 'produto/detail.html'
    context_object_name = 'produto'


class AddAoCarrinho(View):
    def get(self, *args, **kwargs):

        # if self.request.session['carrinho']:
        #     del self.request.session['carrinho']

        http_referer = self.request.META.get(
                'HTTP_REFERER', reverse('produto:list'))
        id_variacao = self.request.GET.get('id_variacao')

        # Levanta um erro caso ao buscar produto inexistente pela url
        if not id_variacao:
            messages.error(self.request, 'Produto não existe')
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, id=id_variacao)
        produto = variacao.produto
        estoque = variacao.estoque

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome
        preco_unitario = variacao.preco
        preco_unitario_promo = variacao.preco_promocional
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if estoque < 1:
            messages.error(self.request, 'Estoque insuficiente')
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session['carrinho']

        if id_variacao in carrinho:
            quantidade_carrinho = carrinho[id_variacao]['quantidade']

            if self.request.GET.get('menos'):
                if quantidade_carrinho <= 1:
                    messages.info(self.request, 'O mínimo é 1 unidade')
                    return redirect(http_referer)
                quantidade_carrinho -= 1
            else:
                if self.request.GET.get('mais'):
                    if estoque == quantidade_carrinho:
                        messages.info(self.request, 'Quantidade \
                            máxima disponível atingida')
                        return redirect(http_referer)
                quantidade_carrinho += 1

            if estoque < quantidade_carrinho:
                messages.info(self.request, f'Temos apenas {estoque}x \
                                unidades disponíveis')
                # return redirect(http_referer)
                quantidade_carrinho = estoque

            carrinho[id_variacao]['quantidade'] = quantidade_carrinho

            carrinho[id_variacao]['preco_quantitativo'] = \
                preco_unitario * quantidade_carrinho

            carrinho[id_variacao]['preco_quantitativo_promo'] = \
                preco_unitario_promo * quantidade_carrinho

        else:
            carrinho[id_variacao] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'id_variacao': id_variacao,
                'preco_unitario': preco_unitario,
                'preco_unitario_promo': preco_unitario_promo,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promo': preco_unitario_promo,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(self.request, 'Item adicionado ao carrinho')
        return redirect('produto:carrinho')


class RemoveDoCarrinho(View):
    def get(self, *args, **kwargs):
        id = self.request.GET.get('id_variacao')

        carrinho = self.request.session['carrinho']

        if id in carrinho:
            del self.request.session['carrinho'][id]
            self.request.session.save()
        messages.success(self.request, 'Produto removido do seu carrinho')
        return redirect('produto:carrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):
        # if self.request.session['carrinho']:
        #     del self.request.session['carrinho']

        carrinho = self.request.session.get('carrinho', {})

        ctx = {
            'carrinho': carrinho,
        }

        return render(self.request, 'produto/carrinho.html', ctx)


class LimparCarrinho(View):
    def get(self, *args, **kwargs):
        del self.request.session['carrinho']
        return redirect('produto:carrinho')


class ResumoDaCompra(View):
    def get(self, *args, **kwargs):
        carrinho = self.request.session.get('carrinho', {})

        if not carrinho:
            return redirect('/')

        ctx = {
            'usuario': self.request.user,
            'carrinho': carrinho,
            'endereco': Endereco.objects.filter(user=self.request.user).filter(padrao=True).first()   
        }
        return render(self.request, 'produto/resumo.html', context=ctx)



class Finalizar(View):
    pass
