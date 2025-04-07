from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ProductForm, ModelForm 
from .models import Product,  ProductModel, Model
from django.views.generic import UpdateView
from django.forms import inlineformset_factory
from django import forms
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.forms.models import modelformset_factory
from django.urls import reverse_lazy
from django.core.paginator import Paginator


# Verifica si el usuario es admin
def is_admin(user):
    return user.is_staff

# Vista para agregar productos (solo admin)
@login_required
@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        
        # Verificar si el formulario es válido
        if product_form.is_valid():
            price = product_form.cleaned_data.get('price')
            
            # Validar que el precio sea positivo
            if price is None or price < 0:
                product_form.add_error('price', 'El precio no puede ser un valor negativo.')
                return render(request, 'add_product.html', {'product_form': product_form})

            # Guardar el producto
            product = product_form.save(commit=False)
            product.is_active = True  # Garantiza que el producto se active
            product.save()

            # Asociar modelos seleccionados
            models = product_form.cleaned_data['models']
            for model in models:
                ProductModel.objects.create(product=product, model=model)

            return redirect('admin_catalog')
    else:
        product_form = ProductForm()

    return render(request, 'add_product.html', {'product_form': product_form})

    
#Vista para cambiar el cambio de stado de un producto activado a desactivado y viseversa:
@login_required
@user_passes_test(is_admin)
def toggle_product_status(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_active = not product.is_active
    product.save()
    return redirect('admin_catalog')
    

# Vista para agregar un nuevo modelo
@login_required
@user_passes_test(is_admin)
def add_model(request):
    if request.method == 'POST':
        model_form = ModelForm(request.POST)
        if model_form.is_valid():
            model_form.save()
            return redirect('manage_models')
    else:
        model_form = ModelForm()
    return render(request, 'add_model.html', {'model_form': model_form})


# Vista para gestionar los modelos
@login_required
@user_passes_test(is_admin)
def manage_models(request):
    models = Model.objects.all().order_by('id')
    
    # Crear el paginador
    paginator = Paginator(models, 10)  # 10 productos por página
    page_number = request.GET.get('page')  # Recuperar el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener los productos de la página actual
    return render(request, 'manage_models.html',  {
        'page_obj': page_obj})


# Vista para editar un modelo
@login_required
@user_passes_test(is_admin)
def edit_model(request, model_id):
    model = get_object_or_404(Model, id=model_id)
    if request.method == 'POST':
        model_form = ModelForm(request.POST, instance=model)
        if model_form.is_valid():
            model_form.save()
            return redirect('manage_models')
    else:
        model_form = ModelForm(instance=model)
    return render(request, 'edit_model.html', {'model_form': model_form})


# Vista para eliminar un modelo
@login_required
@user_passes_test(is_admin)
def delete_model(request, model_id):
    model = get_object_or_404(Model, id=model_id)
    model.delete()
    return redirect('manage_models')
    

# Vista para el catálogo del administrador
@login_required
@user_passes_test(is_admin)
def admin_catalog(request):
    # Recuperar productos con modelos relacionados y ordenar por ID
    products = Product.objects.prefetch_related('models__model').order_by('id')
    
    # Obtener parámetros de búsqueda
    size_query = request.GET.get('size', '').strip()
    price_min_query = request.GET.get('price_min', '').strip()
    price_max_query = request.GET.get('price_max', '').strip()
        
    # Filtrar por talla 
    if size_query:
        products = products.filter(size__icontains=size_query)
        
    # Filtrar por precio mínimo
    if price_min_query:
        products = products.filter(price__gte=price_min_query)

    # Filtrar por precio máximo
    if price_max_query:
        products = products.filter(price__lte=price_max_query)
    
    # Crear el paginador
    paginator = Paginator(products, 10)  # 10 productos por página
    page_number = request.GET.get('page')  # Recuperar el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener los productos de la página actual
    context = {
        'page_obj': page_obj,
        'size_query': size_query,
        'price_min_query': price_min_query,  # Para mantener el valor del precio mínimo
        'price_max_query': price_max_query   # Para mantener el valor del precio máximo
    }
    return render(request, 'admin_catalog.html', context)


# Vista para el catálogo del cliente
@login_required
def client_catalog(request):
    # Filtrar productos activos y con stock disponible
    products = Product.objects.filter(is_active=True, stock__gt=0)
    
    # Obtener parámetros de búsqueda
    description_query = request.GET.get('description', '').strip()
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    color_query = request.GET.get('color', '').strip()
    model_query = request.GET.get('model', '').strip()
    size_query = request.GET.get('size', '').strip()
    
    # Filtrar por descripción
    if description_query:
        products = products.filter(description__icontains=description_query)

    # Filtrar por precio
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
    
    # Filtrar por color
    if color_query:
        products = products.filter(models__model__color__icontains=color_query)
        
    # Filtrar por modelo
    if model_query:
        products = products.filter(models__model__description__icontains=model_query)

    # Filtrar por talla
    if size_query:
        products = products.filter(size__icontains=size_query)
    
    # Configurar el paginador (10 productos por página)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    # Pasar los productos paginados al contexto
    context = {
        'page_obj': page_obj,
        'description_query': description_query,  # Mantener el valor en el formulario
        'price_min': price_min,  # Para el filtro de precio mínimo
        'price_max': price_max,  # Para el filtro de precio máximo
        'color_query': color_query,  # Para el filtro de color
        'model_query': model_query,
        'size_query': size_query,
    }
    return render(request, 'client_catalog.html', context)


@user_passes_test(is_admin)
def update_product(request, pk):
    # Obtener el producto actual o devolver un error 404 si no existe
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        # Instanciar el formulario con los datos enviados y el objeto actual
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            price = form.cleaned_data.get('price')

            # Validar que el precio sea positivo
            if price is None or price < 0:
                form.add_error('price', 'El precio no puede ser un valor negativo.')
                return render(request, 'update_product.html', {'form': form, 'product': product})
            
            
            # Guardar el producto con los datos del formulario
            updated_product = form.save(commit=False)
            # Garantiza que el producto se active
            updated_product.is_active = True
            updated_product.save()  # Guardar el producto actualizado

            # Limpiar las asociaciones previas en el modelo intermedio
            ProductModel.objects.filter(product=updated_product).delete()

            # Crear nuevas asociaciones con los modelos seleccionados
            models = form.cleaned_data['models']
            for model in models:
                ProductModel.objects.create(product=updated_product, model=model)

            # Redirigir al catálogo de admin u otra página después de la actualización
            return redirect('admin_catalog')
    else:
        # Instanciar el formulario con los datos del producto actual
        form = ProductForm(instance=product)
        # Preseleccionar los modelos relacionados
        related_models = Model.objects.filter(productmodel__product=product)
        form.fields['models'].initial = related_models

    # Renderizar la plantilla con el formulario
    return render(request, 'update_product.html', {'form': form, 'product': product})


