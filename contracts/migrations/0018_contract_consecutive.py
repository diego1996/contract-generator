# Generated by Django 4.1.1 on 2022-09-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0017_contract_auxiliary_salary_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='consecutive',
            field=models.CharField(default='', max_length=10, unique=True, verbose_name='Consecutivo del contrato'),
        ),
    ]
