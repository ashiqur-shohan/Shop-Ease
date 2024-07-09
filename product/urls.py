from django.urls import path,include
from .views import Home,ProductDetails
urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('product-details/<str:slug>/', ProductDetails.as_view(), name='product-details')
]
