from django.urls import path, include
from django.contrib.auth import views as auth_views

from music.views import send_email_view
from . import views
from .views import logout_user, send_reset_code_view, reset_password_view, google_login, google_callback, slow_down_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('google/login/', google_login, name='google_login'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logoout/', logout_user, name='logout'),
    path('send/', send_email_view, name='send_email'),
    path('captcha/', include('captcha.urls')),
    path('send-reset-code/', send_reset_code_view, name='send_reset_code'),
    path('reset-password/<uuid:code>/', reset_password_view, name='reset_password'),
    path('google/login/callback/', google_callback, name='google_callback'),
    path('slow-down/', slow_down_view, name='slow_down'),
]
