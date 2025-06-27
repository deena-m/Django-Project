from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProductForm
from .models import Product
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect


# Redirect root to login
def home_redirect(request):
    return redirect('login')

# Login View
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user with this email.")
            return redirect('login')

        user_auth = authenticate(request, username=user.username, password=password)
        if user_auth:
            login(request, user_auth)
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect password.")
            return redirect('login')

    return render(request, 'login.html')

# Register View
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Registered successfully. Please login.")
        return redirect('login')

    return render(request, 'register.html')

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Add Product View
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully.")
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

# Dashboard View
def dashboard(request):
    products = Product.objects.all()
    return render(request, 'dashboard.html', {'products': products})

# Optional: success page (not used currently)
def success(request):
    return HttpResponse('Product listed successfully.')

def dashboard(request):
    query = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category:
        products = products.filter(category=category)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'dashboard.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get cart from session or initialize
    cart = request.session.get('cart', {})

    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('dashboard')

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.session.get('wishlist', [])
    if product_id not in wishlist:
        wishlist.append(product_id)
        request.session['wishlist'] = wishlist
        request.session.modified = True 
    return redirect('dashboard')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=int(pid))
        cart_items.append({
            'product': product,
            'quantity': qty,
            'subtotal': qty * product.price
        })
        total_price += qty * product.price

    return render(request, 'cart.html', {
        'products': cart_items,
        'total_price': total_price
    })

 
def view_wishlist(request):
    wishlist_ids = request.session.get('wishlist', [])
    wishlist_products = Product.objects.filter(id__in=wishlist_ids)
    return render(request, 'wishlist.html', {'products': wishlist_products})

def remove_from_wishlist(request, product_id):
    wishlist = request.session.get('wishlist', [])
    if product_id in wishlist:
        wishlist.remove(product_id)
        request.session['wishlist'] = wishlist
        request.session.modified = True
    return redirect('view_wishlist')

def view_cart(request):
    cart = request.session.get('cart', {})

    # 🔧 Convert list to dict if needed (legacy cleanup)
    if isinstance(cart, list):
        cart = {}  # Reset it to an empty dict to avoid errors
        request.session['cart'] = cart

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            products.append({
                'product': product,
                'quantity': quantity
            })
            total_price += product.price * quantity
        except Product.DoesNotExist:
            continue

    return render(request, 'cart.html', {
        'products': products,
        'total_price': total_price
    })

def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        cart[str(product_id)] = quantity
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('dashboard')
