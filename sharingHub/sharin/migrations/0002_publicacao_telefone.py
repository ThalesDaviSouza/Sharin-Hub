# Generated by Django 4.1.1 on 2022-09-16 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicacao',
            name='telefone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
