from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def send_stock_alert(product):
    subject = f"⚠️ Alerta de Stock Bajo: {product.description}"
    message = f"El producto '{product.description}' tiene un stock crítico ({product.stock} unidad). Es necesario reabastecerlo."
    
    # Obtener todos los administradores (usuarios con is_staff=True)
    admin_emails = User.objects.filter(is_staff=True).values_list('email', flat=True)
    
    if admin_emails:
        send_mail(subject, message, settings.EMAIL_HOST_USER, list(admin_emails))
