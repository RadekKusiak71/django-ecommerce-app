from django.db import models
from decimal import Decimal
from typing import Dict


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Sizes(models.Model):
    xs = models.PositiveIntegerField(default=0)
    s = models.PositiveIntegerField(default=0)
    m = models.PositiveIntegerField(default=0)
    l = models.PositiveIntegerField(default=0)
    xl = models.PositiveIntegerField(default=0)

    def get_quantity(self) -> int:
        return self.xs + self.s + self.m + self.l + self.xl

    def get_size_quantity(self, size: str) -> int:
        return getattr(self, size.lower(), 0)

    def get_sizes_dict(self) -> Dict[str, int]:
        return {
            "xs": self.xs,
            "s": self.s,
            "m": self.m,
            "l": self.l,
            "xl": self.xl,
        }


class Promotion(models.Model):
    amount = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self) -> str:
        return f'Promotion created at {self.created_at.strftime('%Y/%m/%d')} till {self.end_date.strftime('%y/%m/%d')}'


class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(max_length=360)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='products/', default='./static/images/default-product-image.png')
    sizes = models.OneToOneField(Sizes, on_delete=models.CASCADE)
    promotion = models.ForeignKey(
        Promotion, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.price}$ quantity {self.get_quantity()}'

    def save(self, *args, **kwargs) -> None:
        if not self.image:
            self.image = './static/images/default-product-image.png'
        super().save(*args, **kwargs)

    def get_quantity(self) -> int:
        return self.sizes.get_quantity()

    def is_available(self) -> bool:
        return self.get_quantity() > 0

    def get_price_after_promotion(self) -> Decimal:
        if self.promotion:
            return self.price - self.price * Decimal(self.promotion.amount) / 100
        return self.price
