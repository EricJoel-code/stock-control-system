from django.urls import path
from . import views
#from .views import ProductUpdateView
#from .views import catalog

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('admin_catalog/', views.admin_catalog, name='admin_catalog'),
    path('client_catalog/', views.client_catalog, name='client_catalog'),
    #path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_product'),
    path('update-product/<int:pk>/', views.update_product, name='update_product'),
    path('manage-model/', views.manage_models, name='manage_models'),
    path('add-model/', views.add_model, name='add_model'),
    path('edit-model/<int:model_id>/', views.edit_model, name='edit_model'),
    path('delete-model/<int:model_id>/', views.delete_model, name='delete_model'),
    path('product/<int:product_id>/toggle_status/', views.toggle_product_status, name='toggle_product_status'),
]
