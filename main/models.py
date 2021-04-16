from django.db import models
from django.core.validators import RegexValidator
from uuid import uuid4
from PIL import Image
from django.urls import reverse
import os

# Create your models here.
class Message(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField(verbose_name='Email Address',
    max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number entered was not correctly formated.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    message = models.TextField()
    is_order = models.BooleanField(default = True)
    date = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Messages'

    def __str__(self):
        if self.is_order:
            return f'Sent by {self.name} - (An Order)'
        return f'Sent by {self.name} - (A Message)'

class Category(models.Model):
    name = models.CharField(max_length = 100)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    still_instock = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default = 0)
    image = models.ImageField(upload_to = 'product_pics')

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, force_insert = False, force_update = False, using=None, **kwargs):
        super().save()
        if self.image.path:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 600:
                output_size = (600,600)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})
