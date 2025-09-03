"""
URL configuration for rent_it project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from home.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/', include('home.urls'), name='home_urls'),
    path('', home, name='index'),
    path("checkout/", include(("checkout.urls", "checkout"), namespace="checkout")),
    path('profile/', include('profiles.urls'), name='profiles_urls'),
    path('items/', include('items.urls'), name='items_urls'),
    path("checkout/", include("checkout.urls")),
    path('reservation/', include('reservation.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
