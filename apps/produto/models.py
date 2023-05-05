from django.db import models
from utils import resize_image
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.nome

    class Meta:
        verbose_name_plural = 'Categorias'


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    categoria = models.ForeignKey(
                                Categoria,
                                on_delete=models.SET_NULL,
                                null=True, blank=True)
    imagem = models.ImageField(
                            upload_to='produto_imagens/%Y/%m',
                            blank=True,
                            null=True)
    slug = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.nome

    def save(self, *args, **kwargs):

        if not self.slug:
            slug = slugify(f'{self.nome}')
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            resize_image(self.imagem, max_image_size)

    def menor_preco_variacao(self):
        variacoes = Variacao.objects.filter(produto_id=self.id)
        cont = 1
        # REFATORAR DPS
        for variacao in variacoes:
            if cont == 1:
                menor = variacao.preco
                cont = 2
                vad = variacao
            elif variacao.preco < menor:
                menor = variacao.preco
                vad = variacao

        return vad


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    preco = models.FloatField()
    preco_promocional = models.FloatField(null=True, blank=True)
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.produto.nome} - {self.nome}'

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
