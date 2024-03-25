from django.test import TestCase
from store.models import Shipping, Order, OrderItem, Cart, CartItem, AnonymousCart, AuthenticatedCart, Sizes, Promotion, Product, Category
from decimal import Decimal
from django.contrib.auth.models import User


class CartTestCase(TestCase):
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
        user = User.objects.create(
            username="testUser", password="testPassword")

        auth_cart = AuthenticatedCart.objects.create(customer=user)
        anonymous_cart = AnonymousCart.objects.create(
            session_key="test_seession_key")
        shipping = Shipping.objects.create(
            street1='test',
            street2='test',
            country='test',
            zip_code='test'
        )

    def test_cart_exists_method_false(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        product = Product.objects.get(id=1)
        self.assertFalse(auth_cart.exists(product, "xs"))

    def test_cart_exists_method_true(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        product = Product.objects.get(id=1)
        CartItem.objects.create(
            product=product,
            quantity=1,
            size='XS',
            cart=auth_cart
        )
        self.assertTrue(auth_cart.exists(product, "xs"))

    def test_is_quantity_available_false(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        product = Product.objects.get(id=1)
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            size='XS',
            cart=auth_cart
        )
        self.assertFalse(cart_item.is_quantity_available())

    def test_is_quantity_available_true(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        product = Product.objects.get(id=1)
        product.sizes.xs += 1
        product.sizes.save()
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            size='XS',
            cart=auth_cart
        )

        self.assertTrue(cart_item.is_quantity_available())

    def test_cart_total_price(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        product = Product.objects.get(id=1)
        product.sizes.xs += 1
        product.sizes.save()
        cart_item = CartItem.objects.create(
            product=product,
            quantity=5,
            size='XS',
            cart=auth_cart
        )
        expected_price = cart_item.quantity * cart_item.product.price
        self.assertEqual(expected_price, auth_cart.get_total_price())

    def test_check_if_items_available_false(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=1),
            quantity=5,
            size='XS',
            cart=auth_cart
        )
        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=2),
            quantity=5,
            size='XS',
            cart=auth_cart
        )

        self.assertFalse(auth_cart.check_if_items_available())

    def test_check_if_items_available_partial(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        sizes = Product.objects.get(id=2).sizes
        sizes.xs += 2
        sizes.save()

        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=1),
            quantity=5,
            size='XS',
            cart=auth_cart
        )
        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=2),
            quantity=2,
            size='XS',
            cart=auth_cart
        )

        self.assertFalse(auth_cart.check_if_items_available())

    def test_check_if_items_available_true(self):

        auth_cart = AuthenticatedCart.objects.get(id=1)
        sizes = Product.objects.get(id=2).sizes
        sizes.xs += 2
        sizes.save()

        sizes = Product.objects.get(id=1).sizes
        sizes.xs += 2
        sizes.save()

        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=1),
            quantity=2,
            size='XS',
            cart=auth_cart
        )
        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=2),
            quantity=2,
            size='XS',
            cart=auth_cart
        )

        self.assertTrue(auth_cart.check_if_items_available())

    def test_convert_items_into_order_items(self):
        auth_cart = AuthenticatedCart.objects.get(id=1)
        sizes = Product.objects.get(id=2).sizes
        sizes.xs += 2
        sizes.save()

        sizes = Product.objects.get(id=1).sizes
        sizes.xs += 2
        sizes.save()

        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=1),
            quantity=2,
            size='XS',
            cart=auth_cart
        )
        cart_item = CartItem.objects.create(
            product=Product.objects.get(id=2),
            quantity=2,
            size='XS',
            cart=auth_cart
        )

        shipping = Shipping.objects.get(id=1)
        order = Order.objects.create(shipping=shipping,
                                     total=auth_cart.get_total_price(),
                                     status='prepared')

        auth_cart.convert_items_into_order_items(order)

        self.assertEqual(len(OrderItem.objects.filter(order=order)), 2)
