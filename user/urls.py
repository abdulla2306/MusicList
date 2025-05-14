from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import logout_user

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logoout/', logout_user, name='logout'),
]
