from typing import Any, Dict
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from store.models import Product, Cart, CartItem, AnonymousCart, AuthenticatedCart
from django.views import generic
from django.views.generic.base import RedirectView
from django.contrib import messages
from django.shortcuts import redirect


class ProductView(generic.DetailView, RedirectView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['sizes'] = self.get_product_sizes()
        context['slider_items'] = self.get_slider_items()
        return context

    def get_slider_items(self) -> QuerySet[Product]:
        products = Product.objects.filter(
            category=self.get_object().category).exclude(id=self.get_object().id)[:3]
        if not products:
            products = Product.objects.all()[:3]
        return products

    def get_product_sizes(self) -> Dict[str, int]:
        return self.get_object().sizes.get_sizes_dict()

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        form_dict = self.request.POST
        size = form_dict.get("size")
        product = self.get_object()

        if product.sizes.get_size_quantity(size) == 0:
            messages.error(request, "Size is unavailable...")
            return redirect("product-page", pk=product.id)

        if request.user.is_authenticated:
            cart, created_cart = AuthenticatedCart.objects.get_or_create(
                customer=request.user)
        else:
            if not request.session.exists(request.session.session_key):
                request.session.create()
            cart, created_cart = AnonymousCart.objects.get_or_create(
                session_key=request.session.session_key
            )

        if cart.exists(product, size):
            cart_item = CartItem.objects.get(
                cart=cart, product=product, size=size.upper())
            cart_item.quantity += 1
            cart_item.save()
        else:
            CartItem.objects.create(
                cart=cart, product=product, size=size.upper(), quantity=1)

        return redirect("cart-page")
