from django.shortcuts import render,redirect, get_object_or_404 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy

from .models import ProfileModel,Product,Order, Rating, Wishlist, Category,OrderProduct
from .forms import CreateUserForm, ProfileUpdateForm,UserUpdateForm

# Create your views here.

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.GET.get('next', reverse_lazy('home'))
            return redirect(next_url)
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
def profile_view(request, username, id):
    user = get_object_or_404(User, username=username, id=id)
    profile = get_object_or_404(ProfileModel, user=user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST or None, instance=user)
        p_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', username=username, id=id)
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
        'username': username, 
        'id': id
    }
    return render(request, 'core/accounts/profile/profile.html', context)

def home(request, category_id=None):
    cart = None
    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(buyer=request.user, status='cart')
        except Order.DoesNotExist:
            pass

    products = Product.objects.all()[:10] if not category_id else \
               Product.objects.filter(category_id=category_id)
    
    context = {
        'cart':cart,
        'products': products,
        'categories': Category.objects.all()[:3],
        'homepage': True,
    }
    return render(request, 'core/home.html',context)

def all_product(request, category_id=None):
    product_list = Product.objects.filter(category_id=category_id) if category_id else \
                   Product.objects.all()
    
    paginator = Paginator(product_list, 25)
    page = request.GET.get('page')
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    
    context = {
        'products': products,
        'categories': Category.objects.all(),
    }
    return render(request, 'core/products/all-product.html',context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product
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
    cart, _ = Order.objects.get_or_create(buyer=request.user, status='cart')
    
    order_product, created = OrderProduct.objects.get_or_create(
        order=cart,
        product=product,
        defaults={'price_at_purchase': product.price, 'quantity': 1}
    )
    if not created:
        order_product.quantity += 1
        order_product.save()
    
    cart.update_total_price()
    return redirect('all-product')  

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