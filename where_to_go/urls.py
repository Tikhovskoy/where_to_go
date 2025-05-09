from django.contrib import admin
from django.urls import path, include
from core.views import start_page
from places.views import place_detail

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),

    path('', start_page, name='start'),
    path('places/<int:pk>/', place_detail, name='place-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
