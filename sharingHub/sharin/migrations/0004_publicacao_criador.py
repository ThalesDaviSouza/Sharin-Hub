# Generated by Django 4.1.1 on 2022-09-26 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharin', '0003_remove_publicacao_criador'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacao',
            name='criador',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
