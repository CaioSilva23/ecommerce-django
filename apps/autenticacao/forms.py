from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Endereco, DadosUsuario
from utils import strong_password


class RegisterForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label='Nome de usuário',
      
        error_messages={
            'required': 'This field must not be empty',
            'min_length': 'Username must have at least 4 characters',
            'max_length': 'Username must have less than 150 characters',
        },
        min_length=4, max_length=150,
    )
    
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
       
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        error_messages={
            'required': 'Digite a sua senha'
        },
        
        validators=[strong_password],
        label='Senha'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Confirmação de senha',
        error_messages={
            'required': 'Por favor, repita sua senha'
        },
    )

    class Meta:
        model = User
        fields = [
           
            'username',
            'email',
            'password',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'Este email já existe!', code='invalid',
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'As senhas precisam ser iguais',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })


class DadosUsuarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean(self) -> Dict[str, Any]:
        if self.cleaned_data['cpf']:
            cpf = forms.CharField(disabled=True)
            print('foi')
        return super().clean()
    


    class Meta:
        model = DadosUsuario
        fields = "__all__"
        exclude = ('user',)
  

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ('user',)

    def clean(self):
        super().clean()
        if self.cleaned_data['padrao']:
            padrao_antigo = Endereco.objects.filter(padrao=True).first()
            if padrao_antigo:
                padrao_antigo.padrao = False
                padrao_antigo.save()