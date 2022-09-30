from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Publicacao(models.Model):
    criador = models.IntegerField(blank=False, default=1)
    titulo = models.CharField(max_length=32)
    descricao= models.TextField()
    telefone = models.CharField(max_length=12, blank=True, null=True)
    tags = models.TextField()
    data = models.DateField()
    
