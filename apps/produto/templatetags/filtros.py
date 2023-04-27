from django import template

register = template.Library()


@register.filter('formata_preco')
def formata_preco(value):
    return f"R$ {value:_.2f}".replace('.',',').replace('_','.')