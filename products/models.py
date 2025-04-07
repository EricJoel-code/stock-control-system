from django.db import models
from django.core.exceptions import ValidationError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from products.utils import send_stock_alert

class Product(models.Model):
    GENDER_CHOICES = [
        ('male','Masculino'),
        ('female','Femenino'),
        ('unisex', 'Unisex'),
    ]
    
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    stock = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    size = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Verificar si el stock es 1 o menos y enviar alerta
        if self.stock <= 1:
            send_stock_alert(self)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.description


class Model(models.Model):
    description = models.TextField()
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.description} - {self.color}"


class ProductModel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="models")
    model = models.ForeignKey(Model, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product} - {self.model}"