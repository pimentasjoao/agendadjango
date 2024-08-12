from django.shortcuts import render, redirect
from .contact_forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


def register(request):
  form = RegisterForm()

  if request.method=='POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
        name= form.cleaned_data.get('first_name')
        form.save()
        
        messages.success(request, f"O usuario {name} foi registrado")
        return redirect('contact:index')

  
  return render(request, 'contact/register.html',{
    'form': form
  }) 

def login_view(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
       form = AuthenticationForm(request, request.POST)
   
    return render(request, 'contact/login.html',{
    'form': form
  })