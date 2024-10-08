from typing import Any, Dict
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from contact.models import Contact
from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required


class ContactForm(forms.ModelForm):    #criando formulario automatico para ser enviado para o template baseado no Model Contact
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*',}),
        required=False
    )
    class Meta:
        model = Contact   #de qual model sera usado
        fields = (   #quais campos serao renderizados
            'first_name', 'last_name', 'phone',
             'email', 'description', 'category','picture',
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

@login_required(login_url='contact:login')
def create(request):
    form_action=reverse('contact:create')  #metodo reverse serve para desobrir a url de forma reversa dentro de uma view uma que vez que so da para usar {%url %} nos templates

    if request.method =='POST':
        form=ContactForm(request.POST, request.FILES)
        if form.is_valid():  #verifica se passou nas validaçoes
            contact=form.save(commit=False)
            contact.owner=request.user
            contact.save()
            form_action=reverse('contact:update', kwargs= {"contact_id":contact.pk}) #altera para update
            context = {
            'form': form,
            'site_title': 'Create - ',
            'form_action':form_action
            }
            return redirect('contact:update', contact_id=contact.pk)
        else:
            context = {'form': form,'site_title': 'Create - ', 'form_action': form_action} 
            return render(request,'contact/create.html', context,)
    
    else:   #senao meotodo GET, renderiza a pagina em branco
        context = {
        'form': ContactForm(),
        'site_title': 'Create - ',
        'form_action':form_action
        }

        return render(
        request,
        'contact/create.html', context,)
@login_required(login_url='contact:login')
def update(request, contact_id):
    contact=get_object_or_404(Contact, pk=contact_id, show=True, owner=request.user)
    form_action=reverse('contact:update',args=(contact_id,))  

    if request.method =='POST':
        form=ContactForm(request.POST, request.FILES, instance=contact)
        if form.is_valid():  #verifica se passou nas validaçoes
            context = {
            'form': form,
            'site_title': 'Create - ',
            'form_action':form_action
            }
            contact=form.save()
            return redirect('contact:update', contact_id=contact.pk)
        else:
            context = {'form': form,'site_title': 'Update - ', 'form_action': form_action} 
            return render(request,'contact/create.html', context,)
    
    else:   #senao meotodo GET, renderiza a pagina em branco
        context = {
        'form': ContactForm(instance=contact),
        'site_title': 'Update - ',
        'form_action':form_action
        }

        return render(
        request,
        'contact/create.html', context,)
@login_required(login_url='contact:login')    
def delete(request, contact_id):

    contact = get_object_or_404(
        Contact, pk=contact_id, show=True, owner=request.user
    )
    confirmation = request.POST.get('confirmation', 'no')

    if confirmation == 'yes':
        contact.delete()
        return redirect('contact:index')

    return render(
        request,
        'contact/contact.html',
        {
            'contact': contact,
            'confirmation': confirmation,
        }
    )
    
class RegisterForm(UserCreationForm):

    ...
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1