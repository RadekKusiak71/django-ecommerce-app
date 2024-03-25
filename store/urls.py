from django.urls import path
from .views import HomePageView, RegisterCreateView, LoginView, LogoutView

urlpatterns = [
    path('', HomePageView.as_view(), name='home-page'),
    path('register/', RegisterCreateView.as_view(), name='register-page'),
    path('login/', LoginView.as_view(), name='login-page'),
    path('logout/', LogoutView.as_view(), name='logout-page'),
]
