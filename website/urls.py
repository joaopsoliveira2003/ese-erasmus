from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from web.views import *

urlpatterns = [
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('list/<str:name>', list, name='list'),
    path('search/', search, name='search'),
    path('upload-file', file, name='file'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('manage/', admin.site.urls),
    path('error/', error, name="error")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)