# Generated by Django 4.1.1 on 2022-09-21 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0007_alter_contract_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='duration',
            field=models.CharField(default='tres (03) meses', max_length=100, verbose_name='Duración del contrato'),
        ),
    ]
