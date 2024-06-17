"""
URL configuration for deliveet project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('', include('accounts.urls', namespace='accounts')),
    path('', include('customers.urls', namespace='customers')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
