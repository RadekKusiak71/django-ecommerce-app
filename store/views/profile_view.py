from django.views import generic
from store.models import Order, OrderItem, OrderData
from django.contrib.auth import mixins
from django.db.models import QuerySet
from typing import Any


class ProfileOrdersView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'orders.html'

    login_url = 'home-page'
    redirect_field_name = None

    def get_queryset(self) -> QuerySet[Order]:
        profile_queryset = Order.objects.filter(customer=self.request.user)
        return profile_queryset

    def get_context_data(self, **kwargs: mixins) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        print(context)
        return context


class ProfileView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'profile.html'

    login_url = 'home-page'
    redirect_field_name = None

    def get_queryset(self) -> QuerySet[Order]:
        profile_queryset = Order.objects.filter(customer=self.request.user)
        return profile_queryset
