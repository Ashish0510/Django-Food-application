from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class products(models.Model):
     c =(
        ("veg","vegeterian"),("non-veg","non- vegetrian")
    )
    

     name=models.CharField(max_length=100)
     category=models.CharField(max_length=64,choices=c)
     price=models.IntegerField(null=True)
     pic=models.ImageField(upload_to="pro_images/",max_length=250,null=True,default=None)


     def __str__(self):
      return self.name

class profile (models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    token=models.CharField(max_length=150)
    verify=models.BooleanField(default=False) 



class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
      return self.product.name

    @property
    def total_cost(self):
     return int(self.quantity * (self.product.price))





class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    email=models.EmailField(max_length=150,null=True,default=False)
    name=models.CharField(max_length=300,null=True,default=False)
    address=models.CharField(max_length=300,null=True,default=False)
    district=models.CharField(max_length=300,null=True,default=False)
    state=models.CharField(max_length=300,null=True,default=False)
    pincode=models.IntegerField(default=0)

    def __str__(self):
      return self.name

class Orderplaced(models.Model):
    s =(
        ("Order Accepted","Order Accepted"),("Preparing","Preparing"),("Packed","Packed"),("Delivered","Delivered"),("On The Way","On The Way")
    )
    

    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=1)
    status=models.CharField(max_length=64,choices=s)

    @property
    def total_price(self):
        return int(self.quantity * (self.product.price))







