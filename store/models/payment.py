from django.db import models
from .order import Order
import uuid


class Payment(models.Model):
    STATUS_CHOICES = {
        "paid": "paid",
        "unpaid": "unpaid"
    }
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES['unpaid'])
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.status} total: {self.total}$ for order {self.order.id} - {self.created_date.strftime("%Y/%m/%d")}"
