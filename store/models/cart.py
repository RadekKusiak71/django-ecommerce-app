from django.db import models
from django.contrib.auth.models import User
from .item import Item
from .product import Product
from decimal import Decimal
from .order import Order, OrderItem


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    def exists(self, product: Product, size: str) -> bool:
        """
            Method checking if item in cart is already exist
        """
        return CartItem.objects.filter(cart=self, product=product, size=size.upper()).exists()

    def get_total_price(self) -> Decimal:
        cart_items = list(CartItem.objects.filter(cart=self))
        total_price = sum([(item.product.get_price_after_promotion() * item.quantity)
                          for item in cart_items])
        return total_price

    def check_if_items_available(self) -> bool:
        for cart_item in list(CartItem.objects.filter(cart=self)):
            if not cart_item.is_quantity_available():
                return False
        return True

    def convert_items_into_order_items(self, order: Order):
        if not self.check_if_items_available():
            return
        for cart_item in list(CartItem.objects.filter(cart=self)):
            OrderItem.objects.create(
                order=order,
                size=cart_item.size,
                quantity=cart_item.quantity,
                product=cart_item.product
            )


class AnonymousCart(Cart):
    session_key = models.CharField(max_length=200)


class AuthenticatedCart(Cart):
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)


class CartItem(Item):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
