from django.contrib import admin
from .models import Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'price','catg','product_details','is_active']
    list_filter = ['catg','is_active']

admin.site.register(Product,ProductAdmin)


