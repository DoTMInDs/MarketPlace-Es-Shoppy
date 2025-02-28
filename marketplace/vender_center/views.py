from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.decorators import user_passes_test
from core.forms import ProductForm,BecomeSellerForm,CategoryForm,ProductSpecificationForm,SpecificationForm,ProductSpecificationFormSet
from vender_center.models import Seller
from core.models import Product,ProfileModel,Specification,ProductSpecification
from .forms import SellerProfileForm
from django.forms import formset_factory

# Create your views here.
@login_required
def vender_center(request):
    return render(request, 'vender/vender_center.html')

# def add_product(request):
#     if not hasattr(request.user, 'seller'):
#         return redirect('become-seller')
#     form = ProductForm()
#     p_form = CategoryForm()
#     if request.method == "POST":
#         form = ProductForm(request.POST, request.FILES)
#         p_form = CategoryForm(request.POST, request.FILES)
#         if form.is_valid() and p_form.is_valid():
#             instance = form.save(commit=False)
#             instance.seller = Seller.objects.get(user=request.user)
#             instance.save()
#             return redirect('add-product')
#     context = {
#         "form":form,
#         "p_form":p_form,
#     }
#     return render(request, 'vender/add-product.html',context)

def orders(request):
    return render(request, 'vender/orders.html')

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
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductSpecificationFormSet(request.POST, instance=product)
        if product_form.is_valid() and formset.is_valid():
            product_form.save()
            formset.save()
            messages.success(request, 'Product and specifications updated successfully!')
            return redirect('manage-product')  # Redirect to the manage product page or any other page
    else:
        product_form = ProductForm(instance=product)
        formset = ProductSpecificationFormSet(instance=product)
    context = {
        'product_form': product_form, 
        'formset': formset
    }
    return render(request, 'vender/edit-product.html',context)

def add_product(request):
    ProductSpecificationFormSet = formset_factory(ProductSpecificationForm, extra=1)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        spec_formset = ProductSpecificationFormSet(request.POST)
        if product_form.is_valid() and spec_formset.is_valid():
            # Save Product
            product = product_form.save(commit=False)
            product.seller = request.user.seller  # Assuming seller is linked to the user
            product.save()
            for form in spec_formset:
                # Create Specification
                spec_data = {
                    'color': form.cleaned_data.get('color'),
                    'size': form.cleaned_data.get('size'),
                    'weight': form.cleaned_data.get('weight'),
                    'more_details': form.cleaned_data.get('more_details'),
                }
                specification = Specification.objects.create(**spec_data)
                ProductSpecification.objects.create(
                    product=product,
                    specification=specification,
                    features=form.cleaned_data.get('features'),
                    key_features=form.cleaned_data.get('key_features'),
                )
            return redirect('manage-product')  # Redirect to product list
    else:
        product_form = ProductForm()
        spec_formset = ProductSpecificationFormSet()
        
    context = {
        'product_form': product_form,
        'spec_formset': spec_formset,
    }
    return render(request, 'vender/add-product.html',context)

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