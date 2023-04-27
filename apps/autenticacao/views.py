from django.shortcuts import render
from django.views.generic import View



class Login(View):
    def get(self, *args, **kwargs):
        
        return render(self.request, 'login.html')


class Cadastro(View):
    pass


class Logout(View):
    pass

