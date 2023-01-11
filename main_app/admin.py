from django.contrib import admin
from .models import Product, Order, Photo, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Photo)
admin.site.register(Order)
admin.site.register(Cart)
