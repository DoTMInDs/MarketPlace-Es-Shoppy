from django.db import models
from django.contrib.auth.models import User 
from django.core.validators import FileExtensionValidator ,MinValueValidator, MaxValueValidator
from vender_center.models import Seller
from cloudinary.models import CloudinaryField
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # image = CloudinaryField('image', folder='profile_pics',null=True ,blank=True, validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'jfif'])])
    image = models.ImageField( upload_to='profile',blank=True,null=True , validators=[FileExtensionValidator(['png', 'jpg','jpeg', 'WebP', 'jfif'])])
    full_name = models.CharField(blank=True,max_length=200,null=True)
    about = models.TextField(blank=True, null=True)
    talks_about = models.CharField(max_length=255, default='anything',blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = CloudinaryField(folder='categories/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255,null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0.01)])
    canceled_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = CloudinaryField(
        'image',
        folder='products/', 
        blank=True,
        null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,related_name='products') #Added Category
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # updated_at = models.DateTimeField(auto_now=True, null=True)
        
    def average_rating(self):
        ratings = Rating.objects.filter(product=self)
        if ratings.exists():
            return sum(rating.stars for rating in ratings) / ratings.count()
        return 0
    
    @property
    def average_rating(self):
        """Calculate average rating for the product"""
        reviews = self.reviews.all()
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0
    
    @property
    def review_count(self):
        """Get total number of reviews for the product"""
        return self.reviews.count()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='specifications')
    key = models.CharField(max_length=225,null=True,blank=True)
    value = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.key}: {self.value} ({self.product.name})"


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
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='cart')
    cart_items = models.ManyToManyField(Product, through='OrderProduct',related_name='cart_orders')
    # is_archived = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-order_date']
    
    def finalize_order(self):
        """Convert cart to actual order and create seller records"""
        if self.status == 'cart':
            self.status = 'ordered'
            self.save()
            
            self.seller_orders.all().delete()
            
            # Create seller order records
            for item in self.order_products.all():
                SellerOrder.objects.create(
                    seller=item.product.seller,
                    order=self,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price_at_purchase,
                    status='pending'
                )
            self.save()

    def update_total_price(self):
        self.total_price = sum(
            op.price_at_purchase * op.quantity 
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

class SellerOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='orders')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='seller_orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Seller Order"
        verbose_name_plural = "Seller Orders"

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name}"
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    attached_image = CloudinaryField(folder='products/',blank=True,null=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
class Review(models.Model):
    RATING_CHOICES = [
        (1, '★☆☆☆☆ (Poor)'),
        (2, '★★☆☆☆ (Fair)'),
        (3, '★★★☆☆ (Good)'),
        (4, '★★★★☆ (Very Good)'),
        (5, '★★★★★ (Excellent)'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    comment = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'product']  # Each user can review a product only once
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
    
    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name} - {self.rating} stars"
    
    def save(self, *args, **kwargs):
        """Update timestamps and ensure rating is within valid range"""
        if not self.id:  # New review
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        
        # Ensure rating is within bounds
        self.rating = max(1, min(5, self.rating))
        super().save(*args, **kwargs)
    
    @property
    def stars(self):
        """Returns rating as stars (unicode characters)"""
        return '★' * self.rating + '☆' * (5 - self.rating)