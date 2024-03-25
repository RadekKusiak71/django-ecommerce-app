from django.db import models
from .order import Order


class Payment(models.Model):
    STATUS_CHOICES = {
        "paid": "paid",
        "unpaid": "unpaid"
    }

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payment {self.status} total: {self.total}$ for order {self.order.id} - {self.created_date.strftime("%Y/%m/%d")}"
