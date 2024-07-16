"""
URL configuration for deliveet project.
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from deliveet import consumers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls', namespace='pages')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('customer/', include('customers.urls', namespace='customers')),

    path('courier/', include('courier.urls', namespace='couriers')),
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('finance.urls', namespace='finance')),

    path('shipments/', include('shipments.urls', namespace='shipments')),

    path("__reload__/", include("django_browser_reload.urls")),

    path('firebase-messaging-sw.js',
         (TemplateView.as_view(template_name="snippets/firebase-messaging-sw.js",
                               content_type="application/javascript", ))),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

websocket_urlpatterns = [
    path('ws/delivery/<delivery_task_id>/', consumers.DeliveryTaskConsumer.as_asgi()),

]
