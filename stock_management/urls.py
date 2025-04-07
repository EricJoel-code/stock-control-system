"""
URL configuration for stock_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
#from django.conf.urls import handler403
#from products.views import custom_permission_denied_view
#from users import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/',include('orders.urls')),
    # Redirige '/' a la vista de login
    path('', RedirectView.as_view(url='/users/login/', permanent=True)),
    path('__reload__/', include('django_browser_reload.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
