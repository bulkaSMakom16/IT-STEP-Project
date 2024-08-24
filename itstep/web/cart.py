from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'name': product.name,
                'price': str(product.price),
                'quantity': 0,
                'image': str(product.image.url)
            }
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        # Remove the item if the quantity is 0
        if self.cart[product_id]['quantity'] <= 0:
            self.remove_item(product_id)
        else:
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def remove_item(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_total_items(self):
        return sum(item['quantity'] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            cart_item = self.cart[str(product.id)]
            cart_item['product'] = product
            cart_item['id'] = product.id
            cart_item['price'] = Decimal(cart_item['price'])
            cart_item['total_price'] = cart_item['price'] * cart_item['quantity']
            yield cart_item

    def clear(self):
        del self.session['cart']
        self.save()
