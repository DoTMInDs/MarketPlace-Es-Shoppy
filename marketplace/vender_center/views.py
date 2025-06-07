from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import user_passes_test
from core.forms import ProductForm,BecomeSellerForm,CategoryForm,SpecificationFormSet,ProductImageFormSet,ProductImageForm
from vender_center.models import Seller
from django.db import transaction
from core.models import Product,ProfileModel,Order,SellerOrder,ProductSpecification,ProductImage
from .forms import SellerProfileForm
from django.forms import formset_factory

# Create your views here.
@login_required
def vender_center(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vender-center')      
    else:
        form = CategoryForm() 
    
    context = {
        "form":form
    }
    return render(request, 'vender/vender_center.html',context)

# def add_product(request):
#     if not hasattr(request.user, 'seller'):
#         return redirect('become-seller')
   
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = request.user.seller
#             product.save()
#             return redirect('manage-product')
#         else:
#             messages.error(request, "Form validation failed")
#     else:
#         form = ProductForm()
    
#     context = {
#         "form":form,
#         'is_editing': False
#     }
#     return render(request, 'vender/add-product.html',context)

def add_product(request):
    if not hasattr(request.user, 'seller'):
        return redirect('become-seller')

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        formset = SpecificationFormSet(request.POST, prefix='specs')
        image_formset = ProductImageFormSet(request.POST, request.FILES, prefix='images')

        if all([
            form.is_valid(),
            formset.is_valid(),
            image_formset.is_valid()
        ]):
            try:
                with transaction.atomic():
                    # Save main product
                    product = form.save(commit=False)
                    product.seller = request.user.seller
                    product.save()

                    # Save specifications
                    formset.instance = product
                    formset.save()

                    # Save images
                    image_formset.instance = product
                    image_formset.save()
                    messages.success(request, 'Product added successfully!')

                    return redirect('manage-product')

            except Exception as e:
                messages.error(request, f"Error saving product: {str(e)}")
        else:
            messages.error(request, "Please fix the errors below")
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)
            print("Image formset errors:", image_formset.errors)

    else:
        form = ProductForm()
        formset = SpecificationFormSet(prefix='specs') 
        image_formset = ProductImageFormSet(prefix='images') 

    context = {
        "form": form,
        "formset": formset,
        "image_formset": image_formset,
        'is_editing': False
    }
    return render(request, 'vender/add-product.html', context)

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
    # products = Product.objects.filter(seller=seller)
    products = Product.objects.filter(seller=seller).select_related('category')
    
    context = {
        "products":products
    }
    return render(request, 'vender/manage-product.html',context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = SpecificationFormSet(request.POST, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES,instance=product)
        
        if form.is_valid() and formset.is_valid() and image_formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
                image_formset.save()     
            messages.success(request, 'Product updated successfully!')
            return redirect('manage-product') 
    else:
        form = ProductForm(instance=product)
        formset = SpecificationFormSet(instance=product)
        image_formset = ProductImageFormSet(instance=product)
    context = {
        'form': form,
        'formset': formset,
        'image_formset': image_formset,
        'is_editing': True  
    }
    return render(request, 'vender/edit-product.html',context)

def seller_profile(request):
    user = request.user
    if not hasattr(user, 'seller'):
        return redirect('become-seller')
    profile = get_object_or_404(ProfileModel, user=user)
    seller_profile = get_object_or_404(Seller,user=user)
    if request.method == "POST":
        form = SellerProfileForm(request.POST or None, instance=seller_profile)
        if form.is_valid() :
            form.save()
            messages.success(request, 'You have successfully become a seller!')
            return redirect('seller-profile')
    else:
        form = SellerProfileForm(instance=seller_profile)
    
    context = {
        "form":form,
        "profile":profile,
        "seller_profile": seller_profile,
        "user": user,
        
    }
    return render(request, 'seller/seller_profile.html',context)

@login_required
def seller_orders(request):
    try:
        if not hasattr(request.user, 'seller'):
            messages.warning(request, "You need to be a seller to view orders")
            return redirect('home')
            
        seller = request.user.seller
        orders = SellerOrder.objects.filter(seller=seller).select_related('order', 'product').order_by('-created_at')
        
        context = {
            'orders': orders,  # Keep this as 'orders' to match template
            'order_statuses': SellerOrder.STATUS_CHOICES
        }
        return render(request, 'vender/orders.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading orders: {str(e)}")
        return redirect('home')