from django.contrib import admin
from .models import ProfileModel,Category,Product,Order,Rating,OrderProduct,ProductSpecification,SellerOrder,ProductImage
from vender_center.models import Seller


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(Seller)
admin.site.register(OrderProduct)
admin.site.register(ProductSpecification)
admin.site.register(SellerOrder)
admin.site.register(ProductImage)