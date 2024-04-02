from django.db import models
from .product import Product


class Item(models.Model):
    SIZE_CHOICES = {
        "XS": "XS",
        "S": "S",
        "M": "M",
        "L": "L",
        "XL": "XL",
    }

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=3, choices=SIZE_CHOICES)

    class Meta:
        abstract = True

    def is_quantity_available(self) -> bool:
        product_size_quantity = self.product.sizes.get_size_quantity(self.size)
        return product_size_quantity >= self.quantity

    def adjust_quantity(self) -> bool:
        item_count = self.product.sizes.get_size_quantity(self.size)
        if item_count == 0:
            return False
        if item_count < self.quantity:
            self.quantity = item_count
            self.save()
        return True
