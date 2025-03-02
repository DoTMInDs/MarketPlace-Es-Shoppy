from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('login_user/', views.login_user, name='login'),
    path('sign_up/', views.sign_up, name='signup'),
    path('logout_user/', views.logout_user, name='logout'),
    path('profile/<str:username>/<int:id>/', views.profile_view, name='profile'),
    
    path('all_product/', views.all_product, name='all-product'),
    path('all_product/<int:category_id>/', views.all_product, name='all-product'),
    path('product/<int:product_id>/', views.product_detail, name='product-detail'),
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('orders/history/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    # path('orders/clear/', views.clear_order_history, name='clear_history'),
    
    path('update_quantity/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
