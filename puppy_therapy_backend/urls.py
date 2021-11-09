
from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path("api/", include("puppyuser.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

