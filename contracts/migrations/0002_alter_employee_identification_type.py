# Generated by Django 4.1.1 on 2022-09-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='identification_type',
            field=models.CharField(choices=[('CC', 'Cédula de ciudadanía'), ('CE', 'Cédula de extranjería')], default='CC', max_length=3, verbose_name='Tipo de documento'),
        ),
    ]
