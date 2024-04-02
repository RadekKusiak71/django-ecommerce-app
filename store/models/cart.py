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
        cart_items = CartItem.objects.filter(cart=self)
        total_price = 0
        for item in cart_items:
            total_price += item.product.price * item.quantity
        return total_price

    def check_if_items_available(self) -> bool:
        for cart_item in list(CartItem.objects.filter(cart=self)):
            if not cart_item.is_quantity_available():
                return False
        return True

    def adjust_cart_items(self) -> None:
        for cart_item in list(CartItem.objects.filter(cart=self)):
            cart_item.adjust_quantity()

    def convert_items_into_order_items(self, order: Order) -> None:
        for cart_item in list(CartItem.objects.filter(cart=self)):
            product = cart_item.product

            OrderItem.objects.create(
                order=order,
                size=cart_item.size,
                quantity=cart_item.quantity,
                product=product
            )
            product.sizes.take_quantity(cart_item.quantity, cart_item.size)
        self.delete()


class AnonymousCart(Cart):
    session_key = models.CharField(max_length=200)


class AuthenticatedCart(Cart):
    customer = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)


class CartItem(Item):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
