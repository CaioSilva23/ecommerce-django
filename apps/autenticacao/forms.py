from collections import defaultdict
from typing import Any, Dict
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Endereco, DadosUsuario
from django.contrib.auth.forms import UserCreationForm



class RegisterForms(UserCreationForm):
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self) -> Dict[str, Any]:
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Este email já existe')


class DadosUsuarioForm(forms.ModelForm):
    class Meta:
        model = DadosUsuario
        fields = "__all__"
        exclude = ('user',)


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = ('user',)
