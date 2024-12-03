from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.FileField(upload_to='category/images')
    def __str__(self):
        return self.name
    
class Catcategory(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    categoryname=models.CharField(max_length=200, default="")
    def __str__(self):
        return self.categoryname
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default="")
    catcategory=models.ForeignKey(Catcategory,on_delete=models.CASCADE,default="")

    name=models.CharField(max_length=200)
    describein1=models.CharField(max_length=300)
    price=models.IntegerField(default=1)
    image=models.FileField(upload_to='category/images')
    image2=models.FileField(upload_to='category/images')
    instruction1=models.CharField(max_length=200, default="")
    instruction2=models.CharField(max_length=200, default="")
    instruction3=models.CharField(max_length=200, default="")
    instruction4=models.CharField(max_length=200, default="")
    instruction5=models.CharField(max_length=200, default="")
    description=models.TextField(default="")
    def __str__(self):
        return self.name
class Cart(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.IntegerField()

class Wishlist(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    pin_code = models.CharField(max_length=6)
    locality = models.CharField(max_length=255)
    flat_building = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    # address_type = models.CharField(max_length=10, choices=(('Home', 'Home'), ('Work', 'Work'), ('Others', 'Others')))
    # default = models.BooleanField(default=False)
    
  

