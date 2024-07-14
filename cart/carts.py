from django.conf import settings
from product.models import Product
from .models import Coupon

class Cart(object):
    def __init__(self, request) -> None:
        self.session = request.session
        self.cart_id = settings.CART_ID
        self.coupon_id = settings.COUPON_ID
        coupon = self.session.get(self.coupon_id)
        cart = self.session.get(self.cart_id)

        if cart:
            self.cart = cart
        else:
            self.cart = {}
        self.session[self.cart_id] = self.cart

        if coupon:
            self.coupon = coupon
        else:
            self.coupon = None
        self.session[self.coupon_id] = self.coupon

    def update(self, product_id, quantity=1):
        product = Product.objects.get(id=product_id)
        self.session[self.cart_id].setdefault(str(product_id), {'quantity': 0})
        updated_quantity = self.session[self.cart_id][str(product_id)]['quantity'] + quantity
        self.session[self.cart_id][str(product_id)]['quantity'] = updated_quantity
        self.session[self.cart_id][str(product_id)]['subtotal'] = updated_quantity * float(product.price)

        if updated_quantity < 1 :
            del self.session[self.cart_id][str(product_id)]
        self.save()

    def __iter__(self):
        products = Product.objects.filter(id__in=list(self.cart.keys()))
        cart = self.cart.copy()

        for item in products:
            product = Product.objects.get(id=item.id)
            cart[str(item.id)]['product'] = {
                "id": item.id,
                "title": item.title,
                "category": item.category.title,
                "price": float(item.price),
                "thumbnail": item.thumbnail,
                "slug": item.slug
            }
            yield cart[str(item.id)]

    def add_coupon(self, coupon_id):
        self.session[self.coupon_id] = coupon_id
        self.save()

    def save(self):
        self.session.modified = True
    
    def clear(self):
        try:
            del self.session[self.cart_id]
            del self.session[self.coupon_id]
        except:
            pass
        self.save()

    def __len__(self):
        return len(list(self.cart.keys()))

    def total(self):
        amount = 0
        for item in self.cart.values():
            amount += item['subtotal']
        
        if self.coupon:
            coupon = Coupon.objects.get(id=self.coupon)
            amount -= amount * (coupon.discount / 100)
        return amount