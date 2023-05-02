from django.db import models
from django.contrib.auth.models import User
# from utils import cpf_validate
# import re
# from django.forms import ValidationError

estado_choices = (
    ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
    )


class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=4)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(("estado"), max_length=50, choices=estado_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# # Create your models here.
# class Usuario(models.Model):
#     usuario = models.OneToOneField(User, on_delete=models.CASCADE)
#     idade = models.PositiveIntegerField()
#     data_nascimento = models.DateField()
#     cpf = models.CharField(max_length=11)
#     endereco = models.CharField(max_length=50)
#     numero = models.CharField(max_length=5)
#     complemento = models.CharField(max_length=30)
#     bairro = models.CharField(max_length=30)
#     cep = models.CharField(max_length=8)
#     cidade = models.CharField(max_length=30)
#     estado = models.CharField(max_length=2, choices=estado_choices, default='RJ')

#     def __str__(self) -> str:
#         return f'{self.usuario.get_full_name}'

#     def clean(self):
#         error_messages = {}

#         if not cpf_validate(self.cpf):
#             error_messages.update({'cpf': 'Digite um CPF válido'})
#         if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
#             error_messages.update({'cep':'CEP inválido'})

#         if error_messages:
#             raise ValidationError(error_messages)

#     class Meta:
#         verbose_name = 'Perfil'
#         verbose_name_plural = 'Perfis'
