from django.urls import path
from .views import register, CustomLoginView
from users import views

urlpatterns = [
    path('login/', CustomLoginView.as_view(),name='login'),
    path('register/', register, name='register'),
    path('logout/', views.singout, name='logout'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('register-user/', views.register_user, name='register_user'),
]
