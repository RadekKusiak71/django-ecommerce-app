from django.db import models
from django.contrib.auth.models import User
from .item import Item


class Shipping(models.Model):
    street1 = models.CharField(max_length=120)
    street2 = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"Shipping {self.id}"


class OrderData(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} - {self.last_name}'


class Order(models.Model):
    STATUS_CHOICES = {
        "delivered": "delivered",
        "prepared": "prepared",
        "in delivery": "in delivery",
    }

    customer = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    order_data = models.ForeignKey(OrderData, on_delete=models.CASCADE)
    shipping = models.ForeignKey(Shipping, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default=STATUS_CHOICES['prepared'])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order#{self.id} - {self.status} - total: {self.total} - {self.created_at}"


class OrderItem(Item):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
