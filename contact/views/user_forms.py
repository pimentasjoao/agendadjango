from django.shortcuts import render, redirect
from django.urls import reverse
from .contact_forms import RegisterForm, RegisterUpdateForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth


def register(request):
  form = RegisterForm()

  if request.method=='POST':
    form = RegisterForm(request.POST)
    if form.is_valid():
        name= form.cleaned_data.get('first_name')
        form.save()
        
        messages.success(request, f"O usuario {name} foi registrado")
        return redirect('contact:login')

  
  return render(request, 'contact/register.html',{
    'form': form
  }) 

def login_view(request):
    form = AuthenticationForm(request)
    form_action=reverse('contact:login')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            messages.success(request, 'Logado com sucesso!')
            return redirect('contact:index')
        messages.error(request, 'Login inválido')

    return render(
        request,
        'contact/login.html',
        {
            'form': form,
             'form_action': form_action
        }
    )


def logout_view(request):
    auth.logout(request)
    return redirect('contact:login')


def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/user_update.html',
            {
                'form': form
            }
        )

    form.save()
    messages.success(request, 'Dados do usuario foram alterados')
    return redirect('contact:index')

