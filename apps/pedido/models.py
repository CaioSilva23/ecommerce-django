from django.db import models
from django.contrib.auth.models import User

class Pedido(models.Model):
    status_choices = (
        ('A', 'Aprovado'),
        ('C', 'Criado'),
        ('R', 'Reprovado'),
        ('P', 'Pendente'),
        ('E', 'Enviado'),
        ('F', 'Finalizado'),
        )

    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total = models.FloatField()
    qtd_total = models.IntegerField()
    status = models.CharField(max_length=1, choices=status_choices, default='C')

    def __str__(self) -> str:
        return f'Pedido N° {self.pk}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=255)
    produto_id = models.PositiveIntegerField()
    varicao = models.CharField(max_length=255)
    varicao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    def __str__(self) -> str:
        return f'Item do {self.pedido}'
    
    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens do pedido'