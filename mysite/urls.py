"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls")),
    path("api/auth", include("knox.urls")),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('archive/', include('archive.urls')),
    path('profile_page/', include('profile_page.urls')),
    path('finance_data/', include('finance_data.urls')),
    path('send_email/', TemplateView.as_view(template_name="send_email/send_email.html"), name='send_email'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
