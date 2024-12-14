from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class products(models.Model):
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to="product_images")
    options=(
        ("smartPhone","smartPhone"),
        ("Tablet","Tablet"),
        ("SmartWatch","SmartWatch"),
        ("LapTop","Laptop"),
        
    )
    category=models.CharField(max_length=100,choices=options)
    
    
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(default=1)
    
    
class Orders(models.Model):
    product=models.ForeignKey(products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField()
    options=(
        ("OrderPlaced","OrderPlaced"),
        ("Shipped","Shipped"),
        ("OutForDelivery","OutForDelivery"),
        ("Delivered","Delivered"),
        ("Cancelled","Cancelled"),
        
    )
    
    status=models.CharField(max_length=100,default="OrderPlaced",choices=options)
    
    
        
    
