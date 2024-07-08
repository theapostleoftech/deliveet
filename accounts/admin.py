from django.contrib import admin

from accounts.models import UserAccount, Customer, Courier

# Register your models here.
admin.site.register(UserAccount)

admin.site.register(Customer)

admin.site.register(Courier)
