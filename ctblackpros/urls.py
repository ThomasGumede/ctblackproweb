from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('ct-admin/', admin.site.urls),
    path("", include("accounts.urls", namespace="accounts")),
    path("", include("home.urls", namespace="home")),
]
 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)