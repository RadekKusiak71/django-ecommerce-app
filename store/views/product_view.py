from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from store.models import Product, Cart, CartItem, AnonymousCart, AuthenticatedCart
from django.views import generic
from django.urls import reverse_lazy


class ProductView(generic.DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['sizes'] = self.get_product_sizes()
        context['slider-items'] = self.get_slider_items()
        return context

    def get_slider_items(self):
        products = Product.objects.filter(
            category=self.get_object().category)[:3]
        if not products:
            products = Product.objects.all()[:3]
        return products

    def get_product_sizes(self):
        return self.get_object().sizes.get_sizes_dict()
