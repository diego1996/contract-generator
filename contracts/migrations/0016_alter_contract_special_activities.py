# Generated by Django 4.1.1 on 2022-09-25 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0015_remove_employer_letterhead_footer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='special_activities',
            field=models.TextField(default='', max_length=100000, verbose_name='Actividades especiales del contrato'),
        ),
    ]