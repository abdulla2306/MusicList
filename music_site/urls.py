from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user.views import reset_password_view, slow_down_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('slow-down/', slow_down_view),
    path('accounts/', include('user.urls')),
    path('', include('music.urls')),
    path('reset-password/<uuid:token>/', reset_password_view, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
