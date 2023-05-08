from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import DadosUsuario



@receiver(post_save, sender=User)
def create_dados_usuario(sender, instance, created, **kwargs):
    if created:
        dados = DadosUsuario(user=instance)
        dados.save()

