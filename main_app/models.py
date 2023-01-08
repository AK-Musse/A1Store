from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    category =  models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.Case)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Photo(models.Model):
    url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for cat_id: {self.product_id} @{self.url}"
