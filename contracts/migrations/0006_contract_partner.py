# Generated by Django 4.1.1 on 2022-09-21 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_contract_auxiliary_salary_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='partner',
            field=models.CharField(blank=True, max_length=600, null=True, verbose_name='Cliente principal'),
        ),
    ]
