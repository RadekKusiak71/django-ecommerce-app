from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.views import generic
from store.models import Product, Category


class HomePageView(generic.ListView):
    template_name = "home.html"
    model = Product
    paginate_by = 6
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_allow_empty(self) -> bool:
        return super().get_allow_empty()
