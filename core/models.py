from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        unique_together = ['user', 'product']   

    def __str__(self):
        return f"{self.user.username} - {self.product.name} x {self.quantity}"

class Address(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    fullname= models.CharField(max_length=100)
    street= models.CharField(max_length=255)
    city= models.CharField(max_length=100)
    postal_code= models.CharField(max_length=10)
    country= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.fullname} - {self.city}"

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    address= models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    create_at= models.DateTimeField(auto_now_add=True)
    paid= models.BooleanField(default=False)

    def __str__(self):      
        return f"Order #{self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order= models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity= models.PositiveIntegerField()
    price= models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"