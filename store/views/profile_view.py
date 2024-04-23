from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.views import generic
from store.models import Order
from django.contrib.auth import mixins
from django.db.models import QuerySet
from typing import Any
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages


class ProfileOrdersView(mixins.LoginRequiredMixin, generic.ListView):
    template_name = 'orders.html'

    login_url = 'home-page'
    redirect_field_name = None

    def get_queryset(self) -> QuerySet[Order]:
        profile_queryset = Order.objects.filter(customer=self.request.user)
        return profile_queryset

    def get_context_data(self, **kwargs: mixins) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context


class ProfileView(mixins.LoginRequiredMixin, generic.UpdateView):
    template_name = 'profile.html'
    model = User
    login_url = 'home-page'
    redirect_field_name = None
    fields = ("username", "first_name", "last_name")
    success_url = reverse_lazy('profile-page')

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form: BaseModelForm):
        messages.success(self.request, "Account updated")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm):
        messages.error(self.request, "Problem occured while updating account")
        return super().form_invalid(form)
