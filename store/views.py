from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductVariant, Order
from .forms import CheckoutForm

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart = request.session.get('cart', {})
    
    variant_id_str = str(variant_id)
    if variant_id_str in cart:
        cart[variant_id_str] += 1
    else:
        cart[variant_id_str] = 1
        
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for variant_id, quantity in cart.items():
        variant = ProductVariant.objects.get(id=variant_id)
        item_total = variant.price * quantity
        total_price += item_total
        cart_items.append({
            'variant': variant,
            'quantity': quantity,
            'item_total': item_total
        })
        
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Calculate total
            total_price = 0
            for variant_id, quantity in cart.items():
                variant = ProductVariant.objects.get(id=variant_id)
                total_price += variant.price * quantity

            # Create the order
            order = form.save(commit=False)
            order.total_paid = total_price
            order.save()

            # Clear the cart
            request.session['cart'] = {}
            
            return render(request, 'store/checkout_success.html', {'order': order})
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {'form': form})