from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Order, OrderDetail
from django.utils.timezone import now
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# Crear una orden
@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 0))
        if quantity <= 0 or quantity > product.stock:
            messages.error(request, "Cantidad no válida. Verifica el stock disponible.")
        else:
            # 🔥 Crear siempre un nuevo pedido para cada compra 🔥
            order = Order.objects.create(client=request.user, date_order=now())

            # Crear el detalle del pedido
            OrderDetail.objects.create(order=order, product=product, quantity=quantity)

            # Reducir el stock del producto
            product.stock -= quantity
            product.save()

            messages.success(request, f"Pedido realizado con éxito. Puedes cancelarlo o confirmarlo solo dentro de los 5 minutos.")
            return redirect('client_orders')  # Redirigir a la interfaz de los pedidos del cliente

    return render(request, 'create_order.html', {'product': product})

#Cancelar la orden
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)
    order.update_status()

    if not order.is_cancelable:
        messages.error(request, "El tiempo para cancelar este pedido ha expirado.")
    else:
        # Restaurar stock
        for detail in order.order_details.all():
            detail.product.stock += detail.quantity
            detail.product.save()
        # Eliminar pedido
        order.delete()
        messages.success(request, "Pedido cancelado con éxito.")
    
    return redirect('client_orders')


#Confirmar la Orden
@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, client=request.user)
    order.update_status()

    if order.status != 'Pending':
        messages.error(request, "El pedido ya no se puede confirmar.")
    else:
        order.status = 'Confirmed'
        order.is_cancelable = False
        order.save()
        messages.success(request, "Pedido confirmado.")
    
    return redirect('client_orders')


# Despachar el Pedido
@staff_member_required
def dispatch_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.update_status()

    if order.status == 'Confirmed':
        # El pedido ya está confirmado, despacharlo sin considerar el tiempo de cancelación
        order.status = 'Dispatched'
        order.save()
        send_dispatch_email(order)
        messages.success(request, "Pedido despachado con éxito.")
    elif order.status == 'Pending':
        # Si el pedido está pendiente, muestra la advertencia de los 5 minutos
        if now() - order.date_order < timedelta(minutes=5):
            messages.warning(request, "El cliente tiene 5 minutos para cancelar. ¿Desea despachar de inmediato?")
        else:
            # Si ya pasaron los 5 minutos, despachar el pedido
            order.status = 'Dispatched'
            order.save()
            send_dispatch_email(order)
            messages.success(request, "Pedido despachado con éxito.")
    elif order.status == 'Cancelled':
        messages.error(request, "Este pedido ha sido cancelado y no puede ser despachado.")
    else:
        messages.error(request, "El pedido no está listo para ser despachado.")
    
    return redirect('manage_orders')

# Función para enviar correo al cliente
def send_dispatch_email(order):
    subject = "Tu pedido ha sido despachado"
    sender_email = settings.DEFAULT_FROM_EMAIL  # Configura esto en settings.py
    recipient_email = order.client.email  # Asegúrate de que el modelo Order tenga un campo relacionado con el cliente
    
    for detail in order.order_details.all():  # Iterar sobre cada detalle del pedido
        message = f"Hola {order.client.first_name} {order.client.last_name},\n\n"
        message += f"Tu pedido de {detail.quantity} cantidad/es, del producto: {detail.product.description} ha sido despachado y está en camino.\n\n"
        message += "Gracias por tu compra en Daos Sport."

        send_mail(subject, message, sender_email, [recipient_email])

@login_required
def client_orders(request):
    # Obtener todos los pedidos del cliente
    orders = Order.objects.filter(client=request.user).all().order_by('-id')
    
    # Actualizar estado de cada pedido
    for order in orders:
        order.update_status()
        
    # Obtener parámetros de búsqueda
    date_query = request.GET.get('date', '').strip()

    # Filtrar por fecha exacta
    if date_query:
        orders = orders.filter(date_order__date=date_query)

    # Verificar si hay pedidos
    if orders.exists():
        # Calcular el total general de todos los pedidos
        grand_total = sum(
            detail.quantity * detail.product.price
            for order in orders
            for detail in order.order_details.all()
        )
        
# Agregar tiempo restante a cada pedido
        for order in orders:
            order.remaining_time = order.remaining_time()  # Agregar atributo dinámico para la plantilla

        # Configurar el paginador
        paginator = Paginator(orders, 10)  # 10 pedidos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        # Si no hay pedidos
        grand_total = 0
        page_obj = None

    return render(request, 'client_orders.html', {'page_obj': page_obj, 'grand_total': grand_total, 'date_query': date_query })



@staff_member_required
def manage_orders(request):
    orders = Order.objects.select_related('client').prefetch_related('order_details__product').all().order_by('-id')
    
    # Actualizar estado de cada pedido
    for order in orders:
        order.update_status()
    
    # Obtener parámetros de búsqueda
    client_query = request.GET.get('client', '').strip()
    date_query = request.GET.get('date', '').strip()

    # Filtrar por cliente (nombre o apellido)
    if client_query:
        orders = orders.filter(client__first_name__icontains=client_query) | orders.filter(client__last_name__icontains=client_query)

    # Filtrar por fecha exacta
    if date_query:
        orders = orders.filter(date_order__date=date_query)
    
    # Crear el paginador
    paginator = Paginator(orders, 10)  # 10 productos por página
    page_number = request.GET.get('page')  # Recuperar el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener los productos de la página actual
    
    context = {
        'page_obj': page_obj,
        'client_query': client_query,  # Para mantener el valor en el formulario
        'date_query': date_query
    }
    return render(request, 'admin_orders.html', context)

@csrf_exempt  # Desactivar CSRF solo si usas fetch, si usas axios o jQuery, mejor incluir CSRF token.
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id)
            
            # Si el pedido aún está en pendiente, actualizar a confirmado
            if order.status == "Pendiente":
                order.status = "Confirmado"
                order.save()
                return JsonResponse({"success": True, "status": "Confirmado"})
            
            return JsonResponse({"success": False, "message": "El pedido ya está confirmado o cancelado."})

        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Pedido no encontrado."})

    return JsonResponse({"success": False, "message": "Método no permitido."}, status=405)
