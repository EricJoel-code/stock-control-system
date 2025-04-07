from django.urls import path
from .views import create_order, cancel_order, confirm_order, dispatch_order
from .views import client_orders
from .views import manage_orders 
from .views import update_order_status

urlpatterns = [
    path('create/<int:product_id>/', create_order, name='create_order'),
    path('cancel/<int:order_id>/', cancel_order, name='cancel_order'),
    path('confirm/<int:order_id>/', confirm_order, name='confirm_order'),  # Nueva ruta
    path('orders/', client_orders, name='client_orders'),
    path('admin/orders/', manage_orders, name='manage_orders'),
    path('admin/orders/dispatch/<int:order_id>/', dispatch_order, name='dispatch_order'), # Ruta para despachar
    path('update-order-status/<int:order_id>/', update_order_status, name='update_order_status'),
]
