from django.urls import path
from .views import HomePageView, OrderView, RegisterCreateView, CartItemAdd, CartItemDelete, LoginView, LogoutView, ProductView, CartView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('product/<int:pk>/', ProductView.as_view(), name='product-page'),
    path('cart/', CartView.as_view(), name='cart-page'),
    path('cart/<int:pk>/delete/',
         CartItemDelete.as_view(), name='cart-item-delete'),
    path('cart/<int:pk>/add/',
         CartItemAdd.as_view(), name='cart-item-add'),
    path('order/', OrderView.as_view(), name='order-page'),
    path('register/', RegisterCreateView.as_view(), name='register-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout-page'),
]
