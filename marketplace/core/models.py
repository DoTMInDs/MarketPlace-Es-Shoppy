from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator 
from vender_center.models import Seller

# Create your models here.

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.png', upload_to='profile',blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'avif', 'jfif'])])
    full_name = models.CharField(null=True,max_length=200)
    about = models.TextField(null=True)
    talks_about = models.CharField(max_length=255, default='anything', null=True)

    def __str__(self):
        return f'Profile of {self.about}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    canceled_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True) #Added Category
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    specifications = models.ManyToManyField('Specification',through='ProductSpecification',related_name='products')

    def __str__(self):
        return self.name
    
    def average_rating(self):
        ratings = Rating.objects.filter(product=self)
        if ratings.exists():
            return sum(rating.stars for rating in ratings) / ratings.count()
        return 0
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

class Specification(models.Model):
    more_details = models.TextField(null=True,blank=True)
    color = models.CharField(max_length=100,null=True,blank=True)
    brand = models.CharField(max_length=100,null=True,blank=True)
    weight = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.color

class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    features = models.TextField(max_length=255,null=True,blank=True)
    key_features = models.TextField(max_length=255,null=True,blank=True)

    class Meta:
        unique_together = ('product', 'specification')

    def __str__(self):
        return f"{self.specification.color}: {self.product}"

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(choices=[(i, i) for i in range(1, 6)])

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} {self.stars} stars"

class Order(models.Model):
    STATUS_CHOICES = (
        ('cart', 'Cart'),
        ('ordered', 'Ordered'),
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders')
    # products = models.ManyToManyField(Product, through='OrderProduct')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    cart_items = models.ManyToManyField(Product, through='OrderProduct',related_name='cart_orders')

    def update_total_price(self):
        self.total_price = sum(
            op.product.price * op.quantity 
            for op in self.order_products.all()
        )
        self.save()
        
    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username} ({self.status})"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='product_orders')
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'product')

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"