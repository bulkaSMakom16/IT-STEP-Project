from .cart import Cart

def cart(request):
    return {
        'cart': Cart(request)
    }

def cart_count(request):
    cart = Cart(request)
    return {
        'cart_count': cart.get_total_items()
    }