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
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('finance.urls', namespace='finance')),

    path('', include('shipments.urls', namespace='shipments')),

    path("__reload__/", include("django_browser_reload.urls")),
]
