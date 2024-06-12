from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path('api/', include("payment.urls")),
    path('', include('caching.urls')),
    path('api/v1/contact/', include('user_contact_message.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
