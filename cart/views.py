from datetime import datetime
from .carts import Cart
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404,redirect
from django.views import generic
from product.models import Product
from .models import Coupon

class AddtoCart(generic.View):
    def post(self,*args, **kwargs):
        product = get_object_or_404(Product, id = kwargs.get('product_id'))
        cart = Cart(self.request)
        cart.update(product.id,1)
        return redirect('cart')
    
class CartItems(generic.TemplateView):
    template_name = 'cart/cart.html'

    def get(self,request,*args, **kwargs):
        product_id = request.GET.get('product_id',None)
        quantity = request.GET.get('quantity', None)
        clear = request.GET.get('clear', False)
        cart = Cart(request)
        if product_id and quantity:
            product = get_object_or_404(Product,id=product_id)
            if product.in_stock:
                cart.update(int(product_id),int(quantity))
                return redirect('cart')
            else:
                messages.warning(request,'The Product is out of stock')
                return redirect('cart')
        if clear:
            cart.clear()
            return redirect('cart')
        return super().get(request,*args, **kwargs)
    
class AddCoupon(generic.View):
    def post(self,*args, **kwargs):
        code = self.request.POST.get('coupon','')
        coupon = Coupon.objects.filter(code__iexact=code, active = True)
        cart = Cart(self.request)
        
        if coupon.exists():
            coupon = coupon.first()
            current_time = datetime.date(timezone.now())
            active_date = coupon.active_date
            expiry_date = coupon.expiry_date
            if current_time > expiry_date:
                messages.warning(self.request, "Coupon Code has expired.")
                return redirect('cart')
            if current_time < active_date:
                messages.warning(self.request, "Coupon Code has not activated.")
                return redirect('cart')
            if cart.total() < coupon.required_amount_to_use_coupon:
                print(cart)
                messages.warning(self.request, f"You Have to at least shop {
                                 coupon.required_amount_to_use_coupon} to use this coupon code.")
                return redirect('cart')
            messages.success(self.request, "Coupon has been applied.")
            cart.add_coupon(coupon.id)
            return redirect('cart')

        else:

            messages.warning(self.request,"Invalid Coupon Code.")
            return redirect('cart')

