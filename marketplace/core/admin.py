from django.contrib import admin
from .models import ProfileModel,Category,Product,Order,Rating,Wishlist,OrderProduct,ProductSpecification,SellerOrder
from vender_center.models import Seller

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(Wishlist)
admin.site.register(Seller)
admin.site.register(OrderProduct)
admin.site.register(ProductSpecification)
admin.site.register(SellerOrder)