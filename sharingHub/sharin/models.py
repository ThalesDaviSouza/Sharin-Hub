from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class SeparatedValuesField(models.TextField):
#     def __init__(self, *args, **kwargs):
#         self.token = kwargs.pop('token', '#')
#         super(SeparatedValuesField, self).__init__(*args, **kwargs)

#     def to_python(self, value):
#         if not value: return
#         if isinstance(value, list):
#             return value
#         return value.split(self.token)

#     def get_db_prep_value(self, value):
#         if not value: return
#         assert(isinstance(value, list) or isinstance(value, tuple))
#         return self.token.join([unicode(s) for s in value])

#     def value_to_string(self, obj):
#         value = self._get_val_from_obj(obj)
#         return self.get_db_prep_value(value)


# class Instituicao(models.Model):
#     nome = models.CharField(max_length=64)

# class User(models.Model):
#     nome_usuario = models.CharField(max_length=64)
#     senha = models.CharField(max_length=64)
#     email = models.CharField(max_length=100)
#     instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE, related_name="estudantes")
#     telefone = models.CharField(max_length=12)

class Publicacao(models.Model):
    criador = models.IntegerField(blank=False, default=1)
    titulo = models.CharField(max_length=32)
    descricao= models.TextField()
    telefone = models.CharField(max_length=12, blank=True, null=True)
    tags = models.TextField()
    data = models.DateField()
    
