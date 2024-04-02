from django.contrib import admin
from store.models import CartItem, Cart, OrderData, AnonymousCart, AuthenticatedCart, Order, OrderItem, Product, Sizes, Shipping, Category, Promotion, Payment


admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(AnonymousCart)
admin.site.register(AuthenticatedCart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Product)
admin.site.register(Sizes)
admin.site.register(Shipping)
admin.site.register(Category)
admin.site.register(Promotion)
admin.site.register(Payment)
admin.site.register(OrderData)
