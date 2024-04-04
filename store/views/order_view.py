from typing import Any
from django.http import HttpResponse
from django.views import generic
from store.forms import OrderForm
from store.models import AnonymousCart, AuthenticatedCart, Cart, CartItem, Payment
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect


class OrderView(generic.FormView):
    template_name = 'order.html'
    form_class = OrderForm
    success_url = reverse_lazy("home-page")

    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            first_name, last_name = self.request.user.get_full_name().split(" ")
            initial['first_name'] = first_name
            initial['last_name'] = last_name
            initial['email'] = self.request.user.email
        return initial

    """
    {'first_name': 'admin', 
    'last_name': 'admin', 
    'email': 'admin@mail.com', 
    'phone_number': 'asfda', 
    'street1': 'asdadsda',
    'street2': 'adsasd',
    'country': 'asdasdas', 
    'zip_code': 'dasdas'}
    """

    def form_valid(self, form: OrderForm) -> HttpResponse:
        cart = self.get_cart()
        if not cart.check_if_items_available():
            messages.error(
                self.request, "Items are not available... Quantity has been adjusted...")
            cart.adjust_cart_items()
            return redirect('order-page')
        order = form.save()
        cart.convert_items_into_order_items(order)
        Payment.objects.create(order=order, total=order.total)
        return super().form_valid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs.update({'total_price': self.get_cart().get_total_price()})
        return kwargs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        cart = self.get_cart()
        context['cart_items'] = self.get_cart_items(cart)
        context['total_price'] = cart.get_total_price()
        return context

    def get_cart(self):
        if self.request.user.is_authenticated:
            return AuthenticatedCart.objects.get_or_create(customer=self.request.user)[0]
        return AnonymousCart.objects.get_or_create(
            session_key=self.request.session._get_or_create_session_key()
        )[0]

    def get_cart_items(self, cart: Cart):
        queryset = [
            item for item in CartItem.objects.filter(cart=cart) if item.adjust_quantity()]
        return queryset
