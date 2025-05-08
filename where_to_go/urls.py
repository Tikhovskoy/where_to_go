from django.contrib import admin
from django.urls import path
from core.views import start_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='start'),
]
