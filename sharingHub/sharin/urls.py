from django.urls import path
from . import views

app_name = "sharin"

urlpatterns = [
    path("", views.index, name="index"),
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login_view, name="login_view"),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register, name="register"),
    path("perfil/", views.perfil, name="perfil"),
    path("publicacao_view/<publicacao_id>", views.publicacao_view, name="publicacao-view"),
    path("publicacao_edit/<publicacao_id>", views.publicacao_edit, name="publicacao-edit"),
    path("publicacao_delete/<publicacao_id>", views.publicacao_delete, name="publicacao-delete"),
    path("pesquisa_publicacao", views.pesquisa_publicacao, name="pesquisa-publicacao"),
    path('historico', views.historico, name="historico-usuario"),
]