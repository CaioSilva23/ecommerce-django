# Generated by Django 4.1.7 on 2023-05-29 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacao', '0013_endereco_padrao'),
    ]

    operations = [
        migrations.AddField(
            model_name='dadosusuario',
            name='nascimento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='endereco',
            name='padrao',
            field=models.BooleanField(default=False, verbose_name='Endereço padrão'),
        ),
    ]
