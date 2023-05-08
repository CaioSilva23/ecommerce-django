from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils import cpf_validate


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
    cep = models.CharField(max_length=9)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=4)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(("estado"), max_length=50, choices=estado_choices)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.rua}, {self.bairro} - {self.estado}'

    def clean(self):

        error_messages = {}

        if len(self.cep) < 8: # not re.search(r'[^0-9]', self.cep) or
            error_messages.update({'cep': 'Cep inválido'})
        if error_messages:
            raise ValidationError(error_messages)


class DadosUsuario(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    sobrenome = models.CharField(max_length=50, null=True, blank=True)
    cpf = models.CharField(max_length=50, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.nome} {self.sobrenome}'

    class Meta:
        verbose_name = 'Dados de usuário'
        verbose_name_plural = 'Dados dos usuários'

    def clean(self):
        error_messages = {}
        if self.cpf:
            if not cpf_validate(self.cpf):
                error_messages.update({'cpf': 'Digite um CPF válido'})
            if error_messages:
                raise ValidationError(error_messages)
