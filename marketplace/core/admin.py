from django.contrib import admin
from .models import ProfileModel,Category,Product,Order,Rating,OrderProduct,ProductSpecification,SellerOrder,ProductImage,Review
from vender_center.models import Seller


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'created_at', 'updated_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'product__name', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'product')
        }),
        ('Review Details', {
            'fields': ('rating', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

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