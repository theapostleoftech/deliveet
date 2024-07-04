"""
URL configuration for deliveet project.
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('', include('accounts.urls', namespace='accounts')),
    path('customer/', include('customers.urls', namespace='customers')),

    path('courier/', include('customers.urls', namespace='couriers')),
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('finance.urls', namespace='finance')),

    path('shipments/', include('shipments.urls', namespace='shipments')),

    path("__reload__/", include("django_browser_reload.urls")),
]
