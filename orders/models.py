from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  #modelo de usuario predeterminado
from products.models import Product
from datetime import timedelta


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pendiente'),
        ('Confirmed', 'Confirmado'),
        ('Dispatched', 'Despachado'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date_order = models.DateTimeField(default=timezone.now)
    is_cancelable = models.BooleanField(default=True)  # Estado inicial como cancelable
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    
    def update_status(self):
        # Cambia automáticamente a "Confirmado" si pasan los 5 minutos
        if self.status == 'Pending' and self.remaining_time() <= 0:
            self.status = 'Confirmed'
            self.is_cancelable = False
            self.save()
    
    def remaining_time(self):
        """Devuelve el tiempo restante en segundos antes de confirmar automáticamente el pedido."""
        expiration_time = self.date_order + timedelta(minutes=5)
        remaining = (expiration_time - timezone.now()).total_seconds()
        return max(0, int(remaining))  # Evita valores negativos        
            
    def can_dispatch(self):
        """Retorna si el pedido está listo para ser despachado."""
        return self.status == 'Confirmed'
    
    

    def __str__(self):
        return f"Order {self.id} by {self.client.username} - Status: {self.status}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.description} (Order {self.order.id})"
