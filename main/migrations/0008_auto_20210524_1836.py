# Generated by Django 3.1.2 on 2021-05-24 15:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20210515_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
