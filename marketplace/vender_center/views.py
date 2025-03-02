from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import user_passes_test
from core.forms import ProductForm,BecomeSellerForm,CategoryForm,SpecificationFormSet
from vender_center.models import Seller
from core.models import Product,ProfileModel,Order,SellerOrder
from .forms import SellerProfileForm
from django.forms import formset_factory

# Create your views here.
@login_required
def vender_center(request):
    return render(request, 'vender/vender_center.html')

def add_product(request):
    if not hasattr(request.user, 'seller'):
        return redirect('become-seller')
    
    # form = ProductForm()
    # c_form = CategoryForm()
    # product = get_object_or_404(Product, id=product_id) if product_id else None
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = SpecificationFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.save()
            formset.instance = product
            formset.save()
            return redirect('manage-product')
    else:
        form = ProductForm()
        formset = SpecificationFormSet()
    
    context = {
        "form":form,
        'formset': formset,
        'is_editing': False
    }
    return render(request, 'vender/add-product.html',context)

@login_required
def orders(request):
    user_orders = Order.objects.filter(buyer=request.user, status='ordered')
    context = {
        'orders': user_orders
    }
    return render(request, 'vender/orders.html',context)

@login_required
def checkout(request):
    cart = get_object_or_404(Order, buyer=request.user, status='cart')
    cart.finalize_order()  # This creates seller orders
    return redirect('order_confirmation')

@login_required
def become_seller(request):
    # Prevent duplicate seller profiles
    if hasattr(request.user, 'seller'):
        return redirect('vender-center')  # Or your preferred redirect

    if request.method == 'POST':
        form = BecomeSellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            return redirect('vender-center')  # Replace with your URL name
    else:
        form = BecomeSellerForm()

    return render(request, 'seller/become_seller.html', {'form': form})

def manage_product(request):
    seller = Seller.objects.get(user=request.user)
    products = Product.objects.filter(seller=seller)
    
    context = {
        "products":products
    }
    return render(request, 'vender/manage-product.html',context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = SpecificationFormSet(request.POST, instance=product)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Product and specifications updated successfully!')
            return redirect('manage-product')  # Redirect to the manage product page or any other page
    else:
        form = ProductForm(instance=product)
        formset = SpecificationFormSet(instance=product)
    context = {
        'form': form,
        'formset': formset,
        'is_editing': True  
    }
    return render(request, 'vender/edit-product.html',context)

def seller_profile(request,username, id):
    user = get_object_or_404(User, username=username, id=id)
    if not hasattr(user, 'seller'):
        return redirect('become-seller')
    profile = get_object_or_404(ProfileModel, user=user)
    seller_profile = get_object_or_404(Seller,user=user)
    if request.method == "POST":
        form = SellerProfileForm(request.POST or None, instance=seller_profile)
        if form.is_valid() :
            form.save()
            messages.success(request, 'You have successfully become a seller!')
            return redirect('seller-profile',username=user.username, id=user.id)
    else:
        form = SellerProfileForm(instance=seller_profile)
    
    context = {
        "form":form,
        "profile":profile,
        "seller_profile": seller_profile,
        "user": user,
        'username': username, 
        'id': id
    }
    return render(request, 'seller/seller_profile.html',context)

@login_required
def seller_orders(request):
    try:
        if not hasattr(request.user, 'seller'):
            messages.warning(request, "You need to be a seller to view orders")
            return redirect('home')
            
        seller = request.user.seller
        orders = SellerOrder.objects.filter(seller=seller)\
            .select_related('order', 'product')\
            .order_by('-created_at')
        
        if not orders.exists():
            messages.info(request, "No orders found for your products")
        
        print(f"Found {orders.count()} orders for seller {seller.id}")
        for order in orders:
            print(f"Order {order.id} - Product: {order.product.name}")
            
        context = {
            'orders': orders,
            'order_statuses': SellerOrder.STATUS_CHOICES
        }
        return render(request, 'vender/orders.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading orders: {str(e)}")
        return redirect('home')