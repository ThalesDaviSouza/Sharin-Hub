from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import PublicaForm
from .models import Publicacao
# Create your views here.

def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("sharin:login_view"))

    publicacoes = Publicacao.objects.all()
    publicacoes = Reverse(publicacoes)

    return render(request, "sharin/index.html", {
        'publicacao_list': publicacoes,
    })

def cadastro(request):
    enviado = False
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")

    if request.method == "POST":
        form = PublicaForm(request.POST)
        if form.is_valid():
            publicacao = form.save(commit=False)
            publicacao.criador = request.user.id
            publicacao.data = datetime.datetime.now()
            publicacao.save()
            return HttpResponseRedirect('/sharin/cadastro?enviado=True')
    else:
        form = PublicaForm
        if 'enviado' in  request.GET:
            enviado = True

    return render(request, "sharin/cadastro.html", {
        'form':form,
        'enviado':enviado
    })

def publicacao_view(request, publicacao_id):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")

    publicacao = Publicacao.objects.get(pk=publicacao_id)
    criador = User.objects.get(pk=publicacao.criador)
    return render(request, "sharin/publicacao_view.html", {
        "publicacao":publicacao,
        "criador":criador,
    })

def publicacao_edit(request, publicacao_id):
    atualizado = False

    if not request.user.is_authenticated:
        return redirect("sharin:login_view")
    
    publicacao = Publicacao.objects.get(pk=publicacao_id)
    form = PublicaForm(request.POST or None, instance=publicacao)

    if form.is_valid():
        form.save()
        atualizado = True

    

    return render(request, "sharin/publicacao_edit.html", {
        "publicacao":publicacao,
        "form":form,
        "atualizado":atualizado,
    })


def login_view(request):
    if request.method == "POST":
        nome_usuario = request.POST["nome_usuario"]
        senha = request.POST["senha"]
        user = authenticate(request, username=nome_usuario, password=senha)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("sharin:index")) 
        else:
            return render(request, "sharin/login.html", {
                "message":"Usuário ou senha inválidos."
            })

    return render(request, "sharin/login.html")

def register(request):
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        primeiro_nome = request.POST["primeiro_nome"]
        ultimo_nome = request.POST["ultimo_nome"]
        nome_usuario = request.POST["nome_usuario"]
        email = request.POST["email"]
        senha = request.POST["senha"]
        confirmacao_senha = request.POST["confirmacao_senha"]

        if senha == confirmacao_senha:
            if User.objects.filter(username=nome_usuario).exists():
                messages.info(request, "Nome de usuário já utilizado.")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email já está sendo utilizado")
            
            else:
                user = User.objects.create_user(username=nome_usuario, password=senha, email=email, first_name=primeiro_nome, last_name=ultimo_nome)
                user.save()

                return HttpResponseRedirect(reverse("sharin:index"))
        else:
            messages.info(request, "As senhas não batem.")
            return redirect("sharin:register")
    
    return render(request, "sharin/register.html")


def logout_view(request):
    logout(request)
    return render(request, "sharin/login.html", {
        "message":"Log Out"
    })


def perfil(request):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")
    
    return render(request, "sharin/perfil.html")
