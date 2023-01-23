from django.contrib import admin
from django.urls import path, include
from rpg_encounter.encounters import urls as encounters_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(encounters_urls))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
