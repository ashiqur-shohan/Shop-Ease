from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from django.core.paginator import(
    PageNotAnInteger,
    EmptyPage,
    InvalidPage,
    Paginator
)
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
        context['realted_products']= self.get_object().related_product
        return context
    

class CategoryDetails(generic.DetailView):
    model = Category
    template_name = 'product/category-details.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_object().products.all()
        return context


class CustomPaginator:
    def __init__(self,request,queryset,paginated_by):
        # paginator class dui ta value ney queryset and goto gula data ek page a dekhabe
        self.paginator = Paginator(queryset,paginated_by)
        self.paginated_by = paginated_by
        self.queryset = queryset
        # url theke page number ta grab kortesi. jodi url a page number na thake tahole 1 nibe
        self.page = request.GET.get('page',1)

    def get_queryset(self):
        try:
            # paginator er page method er maddhome shei page number er data grab kortesi
            queryset = self.paginator.page(self.page)
        except PageNotAnInteger:
            queryset = self.paginator.page(1)
        except EmptyPage:
            queryset = self.paginator.page(1)
        except InvalidPage:
            queryset = self.paginator.page(1)
        return queryset


class ProductList(generic.ListView):
    model = Product
    template_name = 'product/product-list.html'
    context_object_name = 'object_list'
    paginate_by = 5
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        page_obj = CustomPaginator(self.request, self.get_queryset(),self.paginate_by)
        queryset = page_obj.get_queryset()
        paginator = page_obj.paginator
        context['object_list'] = queryset
        context['paginator'] = paginator
        return context

class SearchProduct(generic.View):
    def get(self, *args, **kwargs):
        key = self.request.GET.get('key','')
        product = Product.objects.filter(
            Q(title__icontains=key) |
            Q(category__title__icontains=key)
        )
        context = {
            'products':product,
            'key' : key
        }
        return render(self.request,'product/search-products.html',context)