"""inventario URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from core.urls import core_patterns

from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView


urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('core/', include(core_patterns)),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('reset/password_reset/', PasswordResetView.as_view(template_name = 'registration/recuperar_contra.html', email_template_name = 'registration/contra_recuperacion.html'), name='password_reset'),
    path('password_reset_done/' , PasswordResetDoneView.as_view(template_name = 'registration/password_reset_done.html') , name='password_reset_done'),
    path('reset/<uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(template_name='registration/confirmacion_contra.html'), name='password_reset_confirm'),
    path('reset/done',PasswordResetCompleteView.as_view(template_name = 'registration/password_reset_complete.html') ,name= "password_reset_complete"),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    

