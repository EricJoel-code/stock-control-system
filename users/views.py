from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings


# Vista de registro
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Autentica al usuario después de registrarse
            
            # Enviar correo de bienvenida
            subject = "¡Bienvenido a Daos Sport!"
            message = f"Hola {user.username},\n\nTu registro en Daos Sport fue exitoso. Ya puedes iniciar sesión y explorar nuestros productos.\n\nGracias por unirte a nuestra comunidad.\n\nAtentamente,\nEl equipo de Daos Sport"
            send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

            
            messages.success(request, "Registro exitoso. Ahora puedes Inicia Sesión.")
            return redirect('login')  # Cambia a la vista deseada
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


# Vista de login
class CustomLoginView(LoginView):
    template_name = 'login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        # Redirige según el tipo de usuario
        if self.request.user.is_staff:
            return '/products/admin_catalog/'  # Ruta para admin
        else:
            return '/products/client_catalog/'  # Ruta para cliente
        
    def form_invalid(self, form):
        # Si la autenticación falla, renderiza el formulario con un mensaje de error
        return render(self.request, self.template_name, {
            'form': form,
            'error_message': 'Usuario o contraseña incorrectos'
        })


#Cierre de Sesión
def singout(request):
    logout(request)
    return redirect ('login')


# Validación para asegurar que solo los administradores acceden
def is_admin(user):
    return user.is_staff


# Vista para gestionar usuarios
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all().order_by('id')  # Orden descendente por ID
    
    # Crear el paginador
    paginator = Paginator(users, 10)  # 10 productos por página
    page_number = request.GET.get('page')  # Recuperar el número de página de la solicitud
    page_obj = paginator.get_page(page_number)  # Obtener los productos de la página actual
    return render(request, 'manage_users.html',  {
        'page_obj': page_obj})
    #return render(request, 'manage_users.html', {'users': users})


# Vista para editar usuarios
@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.is_active = 'is_active' in request.POST  # Activar/desactivar usuario
        user.is_staff = 'is_staff' in request.POST  # Convertir en admin
        user.save()
        messages.success(request, f'El usuario {user.username} se actualizó correctamente.')
        return redirect('manage_users')
    return render(request, 'edit_user.html', {'user': user})


# Vista para eliminar usuarios
@login_required
@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, f'El usuario {user.username} ha sido eliminado.')
        return redirect('manage_users')
    return render(request, 'delete_user.html', {'user': user})


# Vista de registro de usuarios para el admin
@login_required
@user_passes_test(is_admin)
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        is_active = 'is_active' in request.POST
        is_staff = 'is_staff' in request.POST

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect('manage_users')
        
        # Validar que no exista un usuario con el mismo nombre, apellido y email
        if User.objects.filter(username=username, first_name=first_name, last_name=last_name, email=email).exists():
            messages.error(request, "Ya existe un usuario con el mismo Nombre de Usuario, Nombre, Apellido y Correo electrónico.")
            return redirect('manage_users')

        # Crear el usuario
        try:
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
            )
            user.is_active = is_active
            user.is_staff = is_staff
            user.save()
            messages.success(request, "Usuario registrado exitosamente.")
        except Exception as e:
            messages.error(request, f"Error al registrar el usuario: {e}")
        return redirect('manage_users')