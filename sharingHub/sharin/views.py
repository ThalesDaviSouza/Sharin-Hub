from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout,  get_user_model

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

import re
import datetime

from .models import Publicacao
from .forms import PublicaForm
from .tokens import account_activation_token

# Create your views here.

def Reverse(lst):
    new_lst = lst[::-1]
    return new_lst

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Obrigado por confirmar o seu email. Agora você pode logar na sua conta.")
        return redirect('sharin:login_view')
    else:
        messages.error(request, "O link de ativação é inválido!")


    return redirect('sharin:login_view')


def ativarEmail(request, user, to_email):
    mail_subject = "Ativar a sua conta."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])

    if email.send():
        messages.success(request, f'Senhor(a), {user}, por favor, olhe o seu email {to_email} e click no link de ativação para completar o registro. Obs: talvez esteja na caixa de spam.')
    else:
        messages.error(request, f'Houve um problema para enviar o email para {to_email}, por favor verifique se você digitou corretamente.')

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
            enviado = True
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
    criador = User.objects.get(pk=publicacao.criador)
    form = PublicaForm(request.POST or None, instance=publicacao)

    if form.is_valid():
        form.save()
        atualizado = True

    return render(request, "sharin/publicacao_edit.html", {
        "publicacao":publicacao,
        "form":form,
        "atualizado":atualizado,
        "criador":criador,
    })

def publicacao_delete(request, publicacao_id):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")
    
    publicacao = Publicacao.objects.get(pk=publicacao_id)
    publicacao.delete()
    return redirect("sharin:index")

def pesquisa_publicacao(request):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")

    if request.method == "POST":
        pesquisa = request.POST["pesquisado"]
        resultados = Publicacao.objects.filter(titulo__icontains=pesquisa)

        return render(request, "sharin/pesquisa_publicacao.html", {
            "pesquisa":pesquisa,
            "resultados":resultados,
        })


    return render(request, "sharin/pesquisa_publicacao.html",)


def login_view(request):
    if request.method == "POST":
        nome_usuario = request.POST["nome_usuario"]
        senha = request.POST["senha"]
        user = authenticate(username=nome_usuario, password=senha)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("sharin:index")) 
        
        else:
            user = User.objects.get(username=nome_usuario)
            if user and not user.is_active:
                messages.error(request, "Email ainda não foi ativado.")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
            return render(request, "sharin/login.html", {})


    return render(request, "sharin/login.html")

def register(request):
    primeiro_nome = ''
    ultimo_nome = ''
    nome_usuario = ''
    email = ''

    string = '2020951574@teiacoltec.org'
    pattern = re.compile('^[\d]{10}@teiacoltec.org')
    
    if request.user.is_authenticated:
        logout(request)

    if request.method == "POST":
        primeiro_nome = request.POST["primeiro_nome"]
        ultimo_nome = request.POST["ultimo_nome"]
        nome_usuario = request.POST["nome_usuario"]
        email = request.POST["email"]
        senha = request.POST["senha"]
        confirmacao_senha = request.POST["confirmacao_senha"]
        test = re.fullmatch(pattern, email)

        if senha == confirmacao_senha:
            if User.objects.filter(username=nome_usuario).exists():
                messages.info(request, "Nome de usuário já utilizado.")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email já está sendo utilizado.")

            elif re.fullmatch(pattern, email) == None:
                messages.info(request, "Email em formato inválido. Tente usar o email do teiacoltec.")

            else:
                user = User.objects.create_user(username=nome_usuario, password=senha, email=email, first_name=primeiro_nome, last_name=ultimo_nome)
                user.is_active = False
                user.save()
                ativarEmail(request, user, email)

                return redirect('sharin:login_view')
        else:
            messages.info(request, "As senhas não batem.", {
                'primeiro_nome': primeiro_nome,
                'ultimo_nome': ultimo_nome,
                'nome_usuario': nome_usuario,
                'email': email,
            })
            return render(request, "sharin/register.html", {})
    return render(request, "sharin/register.html", {
        'primeiro_nome': primeiro_nome,
        'ultimo_nome': ultimo_nome,
        'nome_usuario': nome_usuario,
        'email': email,
    })

def sendEmail(request):
    password = request.POST.get('password')
    username = request.POST.get('username')
    email = request.POST.get('email')
    user = get_user_model().objects.create(username= username, password = password, email=email)
    sendConfirm(user)
    return render(request, 'email/confirm_template.html')



def logout_view(request):
    logout(request)
    return render(request, "sharin/login.html", {
        "message":"Log Out"
    })


def perfil(request):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")
    
    publicacoes = Publicacao.objects.all().filter(criador=request.user.id)
    
    return render(request, "sharin/perfil.html", {
        "publicacoes":publicacoes,
    })

def historico(request):
    if not request.user.is_authenticated:
        return redirect("sharin:login_view")

    publicacoes = Publicacao.objects.all().filter(criador=request.user.id)

    return render(request, "sharin/historico.html", {
        "publicacoes": publicacoes,
    })
