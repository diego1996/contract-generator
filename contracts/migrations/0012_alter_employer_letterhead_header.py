# Generated by Django 4.1.1 on 2022-09-23 07:03

import contracts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0011_remove_employer_letterhead_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='letterhead_header',
            field=models.FileField(blank=True, null=True, upload_to=contracts.models.get_letterhead_upload_path, verbose_name='Membrete para documentos (cabecera)'),
        ),
    ]
