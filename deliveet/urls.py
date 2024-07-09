"""
URL configuration for deliveet project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

from deliveet.utils import consumers

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

    path('firebase.js',
         (TemplateView.as_view(template_name="snippets/firebase.js", content_type="application/javascript", ))),
]

websocket_urlpatterns = [
                            # path('ws/shipments/<delivery_task_id>/', consumers.ShipmentOrderConsumer.as_asgi())
                            re_path(r'ws/shipments/(?P<delivery_task_id>[\w-]+)/$',
                                    consumers.ShipmentOrderConsumer.as_asgi()),

                        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
