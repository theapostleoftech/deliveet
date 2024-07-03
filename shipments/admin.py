from django.contrib import admin

from shipments.models import Delivery, DeliveryTransaction

# Register your models here.
admin.site.register(Delivery)
admin.site.register(DeliveryTransaction)
