# Generated by Django 3.1.2 on 2021-05-14 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210514_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image2',
            field=models.ImageField(default='default.png', upload_to='product_pics'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image3',
            field=models.ImageField(default='default.png', upload_to='product_pics'),
        ),
    ]
