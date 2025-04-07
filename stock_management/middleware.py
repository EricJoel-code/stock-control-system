from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.contrib.auth import logout

class AdminRestrictionMiddleware(MiddlewareMixin):
    ADMIN_PATHS = [
        "/products/add/",
        "/products/manage-model/",
        "/orders/admin/orders/",
        "/users/manage-users/",
        "/products/admin_catalog/",
        "/products/update-product/",
    ]

    def process_request(self, request):
        """Intercepta las solicitudes antes de que lleguen a la vista."""

        # Bloquea rutas de admin si el usuario no es staff y si no esta autenticado redirige a login
        if request.path in self.ADMIN_PATHS:
            # Si el usuario no está autenticado, redirigir al login
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")
            
            # Si el usuario no es admin, mostrar error 403
            if not request.user.is_staff:
                logout_url = reverse('logout')  # Obtener la URL de logout
                return render(request, "errors/403.html", {"logout_url": logout_url}, status=403)
