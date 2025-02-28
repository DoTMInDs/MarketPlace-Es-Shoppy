from django.urls import path
from . import views

urlpatterns = [
    path('become_seller/', views.become_seller, name='become-seller'),
    path('vender_center/', views.vender_center, name='vender-center'),
    # path('add_product/', views.add_product, name='add-product'),
    path('orders/', views.orders, name='orders'),
    path('manage_product/', views.manage_product, name='manage-product'),
    path('add_product/', views.add_product, name='add-product'),
    path('seller_profile/<str:username>/<int:id>/', views.seller_profile, name='seller-profile'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit-product'),
    
]
