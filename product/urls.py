from django.urls import path,include
from .views import Home,ProductDetails,CategoryDetails,ProductList
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('product-details/<str:slug>/', ProductDetails.as_view(), name='product-details'),
    path('category-details/<str:slug>/', CategoryDetails.as_view(), name='category-details'),
    path('product-list/', ProductList.as_view(), name='product-list'),
]
