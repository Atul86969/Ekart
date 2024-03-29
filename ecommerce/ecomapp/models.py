from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    CAT=((1,'Mobile'),(2,'Shoes'),(3,'Cloths'))
    name = models.CharField(max_length=50, verbose_name = "Product Name" )
    price = models.IntegerField()
    catg = models.IntegerField(verbose_name = "Category", choices=CAT)
    product_details = models.CharField(max_length=500, verbose_name = "Product Details")
    is_active = models.BooleanField(default=True, verbose_name = "Available")
    img = models.ImageField(upload_to='image')

    
    # def __str__(self):
    #     return self.name + " -₹" + str(self.price)


class Cart(models.Model):
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product', on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default = 1)

    
class Order(models.Model):
    order_id = models.CharField(max_length = 100)
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product', on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default = 1)
    amt=models.FloatField()

class MyOrder(models.Model):
    order_id = models.CharField(max_length = 100)
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    pid=models.ForeignKey('Product', on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default = 1)
    amt=models.FloatField()


