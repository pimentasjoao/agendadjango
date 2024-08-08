from typing import Any, Dict

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
        )
        widgets = {    #como serao renderizados
            'first_name': forms.TextInput(
                attrs={
                    'class': 'classe-a classe-b',
                    'placeholder': 'Escreva aqui',
                }
            )
        }

def create(request):
    if request.method =='POST':
        context = {
        'form': ContactForm(request.POST),
        'site_title': 'Create - '
        }
    else:
        context = {
        'form': ContactForm(),
        'site_title': 'Create - '
        }
    
    
    return render(
        request,
        'contact/create.html', context,
    )