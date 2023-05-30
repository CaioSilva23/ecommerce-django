from django import template

register = template.Library()


@register.filter('formata_preco')
def formata_preco(value):
    return f"R$ {value:_.2f}".replace('.',',').replace('_','.')


@register.filter('total_carrinho')
def total_carrinho(carrinho):
    return sum(i['preco_quantitativo_promo'] for i in carrinho.values())