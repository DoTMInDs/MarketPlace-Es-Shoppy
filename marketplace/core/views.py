from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
import cloudinary
import cloudinary.uploader

from .models import ProfileModel,Product,Order, Rating, Category,OrderProduct,ProductSpecification,Review
from .forms import CreateUserForm, ProfileUpdateForm,UserUpdateForm,ReviewForm
from vender_center.models import Seller

# Create your views here.

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home')
        messages.error(request, "Please input a valid username and password")
       
    return render(request, 'core/accounts/user/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
    
def sign_up(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUserForm()
       
    context = {'form':form}
    return render(request, 'core/accounts/user/signup.html', context)

@login_required
def profile_view(request):
    user = request.user
    profile, created = ProfileModel.objects.get_or_create(user=user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST or None, instance=user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
        
    }
    return render(request, 'core/accounts/profile/profile.html', context)

def home(request, category_id=None):
    products = Product.objects.all()
    cart = None
    search_query = request.GET.get('search', '')
    
    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(buyer=request.user, status='cart')
        except Order.DoesNotExist:
            pass

    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    if category_id:
        products = products.filter(category__id=category_id)
    if not search_query and not category_id:
        products = products[:10]
    
    context = {
        'cart':cart,
        'products': products,
        'categories': Category.objects.all()[:3],
        'homepage': True,
    }
    return render(request, 'core/home.html',context)

def all_product(request, category_id=None):
    filter_query = request.GET.get('search', '')
    product_list = Product.objects.all()
    
    # Apply category filter if present
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        product_list = product_list.filter(category_id=category_id)
    
    # Apply search filter if query exists
    if filter_query:
        product_list = product_list.filter(
            Q(name__icontains=filter_query) |
            Q(description__icontains=filter_query) |
            Q(category__name__icontains=filter_query) 
        ).distinct()

    # Handle cart separately from pagination
    cart = None
    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(buyer=request.user, status='cart')
        except Order.DoesNotExist:
            pass

    # Pagination logic
    paginator = Paginator(product_list, 14)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'cart': cart,
        'products': products,
        'categories': Category.objects.all(),
        'current_category': category if category_id else None,
        'current_category_id': category_id,
        'search_query': filter_query,
    }
    return render(request, 'core/products/all-product.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    specs = ProductSpecification.objects.filter(product=product)
    reviews = Review.objects.filter(product=product).order_by('-created_at')
    cart = None
    
    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(buyer=request.user, status='cart')
        except Order.DoesNotExist:
            pass
        
    context = {
        'product': product,
        'cart': cart,
        'specs': specs,
        'reviews': reviews,
    }
    return render(request, 'core/products/product_detail.html', context)

@login_required
def cart_view(request):
    try:
        cart = Order.objects.get(buyer=request.user, status='cart')
    except Order.DoesNotExist:
        cart = None
        
    context = {
        'cart': cart
    }
    return render(request, 'core/products/cart.html', context)

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart, _ = Order.objects.get_or_create(buyer=request.user, status='cart')
    
    order_product, created = OrderProduct.objects.get_or_create(
        order=cart,
        product=product,
        defaults={'price_at_purchase': product.price, 'quantity': quantity}
    )
    if not created:
        order_product.quantity += quantity
        order_product.save()
    
    cart.update_total_price()
    return redirect('all-product')  

def checkout_view(request):
    try:
        profile, _ = ProfileModel.objects.get_or_create(user=request.user)
        cart = Order.objects.get(buyer=request.user, status='cart')
        seller_profile = Seller.objects.get(user=request.user)
    except (ProfileModel.DoesNotExist, Order.DoesNotExist):
        profile = None
        cart = None
        seller_profile = None
    
    context = {
        'profile': profile,
        'cart': cart,
        'seller_profile': seller_profile
    }
    return render(request, "core/products/checkout.html",context)
    
@login_required
def update_quantity(request, item_id, action):
    order_product = get_object_or_404(OrderProduct, id=item_id, order__buyer=request.user)
    
    if action == 'increment':
        order_product.quantity += 1
    elif action == 'decrement' and order_product.quantity > 1:
        order_product.quantity -= 1
        
    order_product.save()
    order_product.order.update_total_price()
    return redirect('cart_view')
    
@login_required
def remove_from_cart(request, item_id):
    order_product = get_object_or_404(OrderProduct, id=item_id, order__buyer=request.user)
    order_product.delete()
    order_product.order.update_total_price()
    return redirect('cart_view')

@login_required
def order_confirmation(request):
    # Get the most recent completed order
    order = Order.objects.filter(
        buyer=request.user,
        status='ordered'
    ).order_by('-order_date').first()
    return render(request, 'core/orders/order_confirmation.html', {'order': order})
        
@login_required
def order_history(request):
    orders = Order.objects.filter(
        buyer=request.user,
        # status='ordered',
        # is_archived=False,
    ).exclude(status='cart').select_related('buyer').order_by('-order_date')
    
    return render(request, 'core/orders/order_history.html', {
        'orders': orders
    }) 

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('buyer')
            .prefetch_related('order_products__product'),
        id=order_id,
        buyer=request.user
    )
    return render(request, 'core/orders/order_details.html', {
        'order': order
    })   

@login_required
def wishlist(request):
    # products = Wishlist.objects.all()
    
    context = {
        # "products":products
    }
    return render(request, "core/products/whishlist.html",context)

@login_required
def reviews_view(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    context = {
        "reviews":reviews
    }
    return render(request, 'core/reviews.html',context)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews')
        else:
            print('there is something wrong')
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'core/edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    if request.method == 'POST':
        product_id = review.product.id
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect('product-detail', product_id=product_id)
    return redirect('reviews')

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    existing_review = Review.objects.filter(user=request.user, product=product).first()
    if request.method == 'POST':
        form = ReviewForm(request.POST,instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('product-detail', product_id=product.id)
        else:
            for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    else:
        form = ReviewForm(instance=existing_review)
    return render(request, 'core/submit_review.html')