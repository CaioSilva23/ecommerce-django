from PIL import Image
import os
from django.conf import settings
import re
from django.core.exceptions import ValidationError


# VALIDADOR DE CPF
def cpf_validate(numbers):
    #  Obtém os números do CPF e ignora outros caracteres
    cpf = [int(char) for char in numbers if char.isdigit()]

    #  Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    #  Verifica se o CPF tem todos os números iguais, ex: 111.111.111-11
    #  Esses CPFs são considerados inválidos mas passam na validação dos dígitos
    #  Antigo código para referência: if all(cpf[i] == cpf[i+1] for i in range (0, len(cpf)-1))
    if cpf == cpf[::-1]:
        return False

    #  Valida os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


# REDIMENCIONA A IMAGEM
def resize_image(img, new_width=800):
    caminho_completo_img = os.path.join(settings.MEDIA_ROOT, img.name)
    img_pil = Image.open(caminho_completo_img)
    original_width, original_height = img_pil.size

    if original_width <= new_width:
        return
    
    new_height = round((new_width * original_height) / original_width)
    new_img = img_pil.resize((new_width, new_height), Image.LANCZOS) 
    new_img.save(
            caminho_completo_img,
            optimize=True,
            quality=50
        )


from django.contrib.auth.models import User

def email_exists(email):
    user_email = User.objects.filter(email=email)
    if user_email.exists():
        raise ValidationError((
            'Este e-mail já existe'
        ))


def confirm_password(password):
    user = User.objects.filter(password=password)



def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'No mínimo 8 caracteres, '
            'possuir pelo menos uma letra minuscula, '
            'uma letra maiúscula e um número'
        ),
            code='invalid'
        )


def email_is_valid(email):
    regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
    )  # noqa: E501
    return bool(re.fullmatch(regex, email))
