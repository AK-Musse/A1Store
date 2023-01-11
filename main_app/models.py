from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORY = (
    ('F','Furniture'),
    ('T','Toy'),
    ('C','Cloth'),
    ('M','Mobile Phone'),
    ('L','Laptop'),
)



class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    category =  models.CharField(
            max_length=1,
            # add the 'choices' field option
            choices=CATEGORY,
            # set the default value for meal to be 'B'
            default=CATEGORY[0][0]
        )

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f'{self.get_category_display()}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.Case)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Photo(models.Model):
    url = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
         
        return f"Photo for cat_id: {self.cat_id} @{self.url}"


class Cart(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    category =  models.CharField(
            max_length=1,
            # add the 'choices' field option
            choices=CATEGORY,
            # set the default value for meal to be 'B'
            default=CATEGORY[0][0]
        )

    def __str__(self):
        # Nice method for obtaining the friendly value of a Field.choice
        return f'{self.get_category_display()}'
