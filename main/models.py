from django.db import models
from django.core.validators import RegexValidator
from uuid import uuid4
from PIL import Image
from django.urls import reverse
from ckeditor.fields import RichTextField

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
    description = RichTextField(blank = True, null = True)
    category = models.ForeignKey(Category, on_delete = models.SET_NULL, null = True)
    still_instock = models.BooleanField(default=True)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(default = 0)
    image1 = models.ImageField(upload_to = 'product_pics')
    image2 = models.ImageField(upload_to = 'product_pics', null=True, default = "default.png")
    image3 = models.ImageField(upload_to = 'product_pics', null=True, default = "default.png")

    class Meta:
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, force_insert = False, force_update = False, using=None, **kwargs):
        super().save()
        if self.image1.path:
            img = Image.open(self.image1.path)

            if img.height > 400 or img.width > 400:
                output_size = (400,400)
                img.thumbnail(output_size)
                img.save(self.image1.path)
        try:
            if self.image2.path:
                img = Image.open(self.image2.path)

                if img.height > 400 or img.width > 400:
                    output_size = (400,400)
                    img.thumbnail(output_size)
                    img.save(self.image2.path)
        except:
            pass
        try:
            if self.image3.path:
                img = Image.open(self.image3.path)

                if img.height > 400 or img.width > 400:
                    output_size = (400,400)
                    img.thumbnail(output_size)
                    img.save(self.image3.path)
        except:
            pass

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})


    def get_image_urls(self):
        urls = []
        try:
            urls.append(self.image2.url)
            urls.append(self.image3.url)
        except:
            pass
        return urls
