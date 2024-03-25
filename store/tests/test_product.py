from django.test import TestCase
from store.models import Sizes, Promotion, Product, Category
from decimal import Decimal
from datetime import datetime


class ProductTestCase(TestCase):
    def setUp(self):
        sizes = Sizes.objects.create()
        sizes2 = Sizes.objects.create()
        category1 = Category.objects.create(title='hoodie')
        category2 = Category.objects.create(title='shirts')
        product1 = Product.objects.create(
            title="test hoodie",
            price=Decimal(100),
            description="test hoodie desc",
            category=category1,
            sizes=sizes,
        )
        product2 = Product.objects.create(
            title="test shirt",
            price=Decimal(19.99),
            description="test shirt desc",
            category=category2,
            sizes=sizes2,
        )

    def test_product_get_quantity_when_0(self):
        self.assertEqual(Product.objects.get(id=1).get_quantity(), 0)

    def test_product_get_quantity_when_1(self):
        product = Product.objects.get(id=1)
        product.sizes.xs += 1
        product.sizes.save()
        self.assertEqual(Product.objects.get(id=1).get_quantity(), 1)

    def test_product_is_not_available(self):
        self.assertFalse(Product.objects.get(id=1).is_available())

    def test_product_deleting_photo(self):
        product = Product.objects.get(id=1)
        product.image = None
        product.save()
        self.assertEqual(
            './static/images/default-product-image.png', product.image)

    def test_price_after_promotion(self):
        promotion = Promotion.objects.create(
            amount=20, end_date=datetime.now())
        product = Product.objects.get(id=1)
        product.promotion = promotion

        self.assertEqual(product.get_price_after_promotion(),
                         product.price - product.price * Decimal(promotion.amount) / 100)

    def test_sizes_get_size_quantity(self):
        sizes = Product.objects.get(id=1).sizes
        self.assertEqual(sizes.xs, sizes.get_size_quantity("Xs"))

    def test_sizes_get_sizes_dict(self):
        sizes = Product.objects.get(id=1).sizes.get_sizes_dict()
        self.assertEqual(sizes, {
            "xs": 0,
            "s": 0,
            "m": 0,
            "l": 0,
            "xl": 0,
        })
