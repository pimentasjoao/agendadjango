from typing import Any, Dict
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from contact.models import Contact


class ContactForm(forms.ModelForm):    #criando formulario automatico para ser enviado para o template baseado no Model Contact
    class Meta:
        model = Contact   #de qual model sera usado
        fields = (   #quais campos serao renderizados
            'first_name', 'last_name', 'phone',
             'email', 'description', 'category',
        )
        widgets = {    #como serao renderizados
            'first_name': forms.TextInput(
                attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': 'Escreva aqui',
                }
            )
        }

    def clean_phone(self):   #validacao do telefone de exemplo, todos os metodos de validação do Django devem iniciar por clean e + nome do campo quando se quer fazer separado
        phone=self.cleaned_data.get('phone')
        if not phone.isdigit() or  not (10 <= len(phone) <= 15):
            raise forms.ValidationError("Este numero nao é um telefone valido",code='invalid')   
        return phone
    
    def clean(self):   #validação quando se usa mais de um campo do post e nao ha problema em fazer junto
        cleaned_data=super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        errors = {}
        if first_name == "JOAO":
            errors['first_name'] = 'Primeiro nome não pode ser JOAO'
        
        if last_name == "ALMEIDA":
            errors['last_name'] = 'Último nome não pode ser ALMEIDA'
        
        if errors:
            raise forms.ValidationError(errors)
        
        return cleaned_data


def create(request):
    if request.method =='POST':
        form=ContactForm(request.POST)
        if form.is_valid():  #verifica se passou nas validaçoes
            context = {
            'form': form,
            'site_title': 'Create - '
            }
            contact=form.save(commit=False)
            contact.show=False
            contact.save()
            return HttpResponse("DEU CERTO")
        else:
            context = {'form': form,'site_title': 'Create - '} 
            return render(request,'contact/create.html', context,)
    
    else:   #senao meotodo GET, renderiza a pagina em branco
        context = {
        'form': ContactForm(),
        'site_title': 'Create - '
        }

        return render(
        request,
        'contact/create.html', context,)

def update(request):
    ...
    

