from django.contrib import admin
from .models import ProfileModel,Category,Product,Order,Rating,Wishlist,OrderProduct, Specification, ProductSpecification
from vender_center.models import Seller

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 2

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSpecificationInline]

class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['color', 'brand', 'weight']
    search_fields = ['color', 'brand', 'weight']

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(Category)
admin.site.register(Product,ProductAdmin)
admin.site.register(Order)
admin.site.register(Rating)
admin.site.register(Wishlist)
admin.site.register(Seller)
admin.site.register(OrderProduct)
admin.site.register(Specification,SpecificationAdmin)
admin.site.register(ProductSpecification)