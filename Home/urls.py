from django.urls import path
from . import views  

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL for the login page
    path('register/', views.register_view, name='register'),  # URL for the registration page
    path('', views.base, name='home'),  # URL for the home page (after login or registration)
]
