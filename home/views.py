from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import TemplateView
from rest_framework import viewsets

from .forms import AddressForm, ReviewForm
from .permissions import IsAuthenticated, IsOwner
from django.contrib.auth.decorators import login_required

from home.models import Address, Category, Pet, CartItem, Cart, Order, OrderItem, Review
from home.serializer import AddressSerializer


class IndexView(TemplateView):
    template_name = 'home/index.html'

    # render index.html

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PetView(TemplateView):
    template_name = 'home/pet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pet_id = kwargs['pk']
        pet = get_object_or_404(Pet, pk=pet_id)
        context['pet'] = pet
        context['reviews'] = pet.reviews.all()
        return context


class CartView(TemplateView):
    template_name = 'home/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.request.user.cart
        return context


@login_required(login_url='/login/')
def add_to_cart(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    print(cart.id, pet.id)
    CartItem.objects.get_or_create(cart=cart, item=pet)

    return redirect('cart')


@login_required(login_url='/login/')
def remove_from_cart(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    cart = request.user.cart
    CartItem.objects.filter(cart=cart, item=pet).delete()

    return redirect('cart')


@login_required(login_url='/login/')
def checkout(request):
    context = {}
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            cart = request.user.cart
            cart_items = cart.items.all()
            order = Order.objects.create(user=request.user, address=address)
            for item in cart_items:
                OrderItem.objects.create(order=order, item=item.item)
            cart.items.all().delete()
            return redirect(f'/order/{order.id}/')
        else:
            return render(request, 'home/checkout.html', {'form': form, })
    else:
        print(request.user)
        if Address.objects.filter(user=request.user).exists():
            address = Address.objects.filter(user=request.user).first()
            print(address)
            context = {"address": address}
        return render(request, 'home/checkout.html', context)


@login_required(login_url='/login/')
def specific_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    for item in order.order_items.all():
        print(item.item.name)
    return render(request, 'home/order.html', {'order': order})


def error_404_view(request, exception):
    return render(request, '404.html')


def error_500_view(request):
    return render(request, '404.html')


class ProductsView(TemplateView):
    template_name = 'home/product.html'

    # render index.html

    def get_context_data(self, **kwargs):
        category = self.request.GET.get('category')

        context = super().get_context_data(**kwargs)
        if category:
            categories = Category.objects.filter(name=category)
        else:
            categories = Category.objects.all()
        context['categories'] = categories
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


class Search(TemplateView):
    """
    implement search with filetering
    1) category
    2) price min max
    3) name search
    4) vaccinated or not

    """
    template_name = 'home/search.html'

    # render index.html

    def get_context_data(self, **kwargs):
        category = self.request.GET.get('category')
        price_min = self.request.GET.get('price_min')
        price_max = self.request.GET.get('price_max')
        name = self.request.GET.get('name')
        vaccinated = self.request.GET.get('vaccinated')

        result = Pet.objects.all()
        if category:
            print(category)
            result = result.filter(category__name=category)
        if price_min:
            result = result.filter(price__gte=price_min)
        if price_max:
            result = result.filter(price__lte=price_max)
        if name:
            result = result.filter(name__icontains=name)
        if vaccinated:
            result = result.filter(vaccinated=vaccinated == 'yes')
        context = super().get_context_data(**kwargs)
        context['products'] = result
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())


@login_required(login_url='/login/')
def review(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.method == 'POST':

        comment = request.POST.get('comment')
        rating = (request.POST.get('rate'))
        print(comment, rating)
        if comment and rating:
            Review.objects.create(user=request.user, pet=pet, comment=comment, rating=rating)

    return redirect(f'/pet/{pet.id}/')
