from django.urls import path
from .views import Login,Logout,Registration
urlpatterns = [
    path('login/',Login.as_view(),name='login'),
    path('logout/',Logout.as_view(),name='logout'),
    path('registration/',Registration.as_view(),name='registration'),
]

