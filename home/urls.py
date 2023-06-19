"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import routers
from home import views

urlpatterns = [
    # register index view
    path('', views.IndexView.as_view(), name='index'),
    # register pet view
    path('pet/<int:pk>/', views.PetView.as_view(), name='pet'),
    # register cart view
    path('cart/', views.CartView.as_view(), name='cart'),
    # add to cart
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    # register order view
    path('checkout/', views.checkout, name='checkout'),
    # register order view
    path('order/<int:pk>/', views.specific_order, name='order'),
]

handler404 = 'home.views.error_404_view'
handler500 = 'home.views.error_500_view'
