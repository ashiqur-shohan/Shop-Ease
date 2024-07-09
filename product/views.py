from django.shortcuts import render
from django.views import generic

from .models import (
    Product,
    Category,
    Slider
)
# Create your views here.

class Home(generic.TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context.update(
            {
                'featured_categories': Category.objects.filter(featured=True),
                'featured_products': Product.objects.filter(featured=True),
                'sliders': Slider.objects.filter(show=True),
            }
        )
        return context

class ProductDetails(generic.DetailView):
    model = Product
    template_name = 'product/product-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context.update(
            {
                'realted_products': self.get_object().related_product
            }
        )
        return context