from .carts import Cart
from django.contrib import messages
from django.shortcuts import get_object_or_404,redirect
from django.views import generic
from product.models import Product
# Create your views here.

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