from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.views import generic
from store.models import AnonymousCart, AuthenticatedCart, Cart, CartItem
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages


class CartView(generic.ListView):
    template_name = 'cart.html'
    model = Cart

    def get_object(self) -> Cart:
        if self.request.user.is_authenticated:
            return AuthenticatedCart.objects.get_or_create(customer=self.request.user)[0]
        return AnonymousCart.objects.get_or_create(
            session_key=self.request.session._get_or_create_session_key()
        )[0]

    def get_queryset(self) -> Cart:
        queryset = [
            item for item in CartItem.objects.filter(cart=self.get_object()) if item.adjust_quantity()]
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['total_cart_price'] = self.get_object().get_total_price()
        return context


class CartItemDelete(generic.DeleteView):
    model = CartItem

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        cart_item: CartItem = self.get_object()
        if cart_item.quantity <= 1:
            cart_item.delete()
        else:
            cart_item.quantity -= 1
            cart_item.save()
        messages.info(
            request, f"{cart_item.product.title} deleted successfully")
        return redirect('cart-page')


class CartItemAdd(generic.UpdateView):
    model = CartItem
    success_url = reverse_lazy('cart-page')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        cart_item: CartItem = self.get_object()
        product_with_correct_size_quantity = cart_item.product.sizes.get_size_quantity(
            cart_item.size)

        if cart_item.quantity + 1 <= product_with_correct_size_quantity:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(
                request, f"{cart_item.product.title} added successfully")
        else:
            messages.info(request, f"Maximum product quantity is {
                          product_with_correct_size_quantity}.")
        return redirect('cart-page')
