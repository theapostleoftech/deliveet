"""
URL configuration for deliveet project - Production Grade API
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from deliveet import consumers

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # REST API v1
    path('api/v1/', include('api.urls', namespace='api')),
    
    # Legacy URLs (Keep for backward compatibility)
    path('', include('pages.urls', namespace='pages')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('customer/', include('customers.urls', namespace='customers')),
    path('courier/', include('courier.urls', namespace='couriers')),
    path('', include('profiles.urls', namespace='profiles')),
    path('', include('finance.urls', namespace='finance')),
    path('shipments/', include('shipments.urls', namespace='shipments')),
    
    # Development tools
    path("__reload__/", include("django_browser_reload.urls")),
    
    # Debug toolbar (development only)
    *([path("__debug__/", include("debug_toolbar.urls"))] if settings.DEBUG else []),
    
    # Static files
    path('firebase-messaging-sw.js',
         (TemplateView.as_view(template_name="snippets/firebase-messaging-sw.js",
                               content_type="application/javascript", ))),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

# WebSocket URL patterns
websocket_urlpatterns = [
    path('ws/delivery/<delivery_task_id>/', consumers.DeliveryTaskConsumer.as_asgi()),
    path('ws/tracker/<shipment_id>/<user_token>/', consumers.DeliveryTrackerConsumer.as_asgi()),
    path('ws/notifications/<user_id>/<user_token>/', consumers.NotificationConsumer.as_asgi()),
]

