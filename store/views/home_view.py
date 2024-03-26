from typing import Any, Dict, List
from django.db.models.query import QuerySet
from django.http.response import HttpResponse as HttpResponse
from django.views import generic
from store.models import Product, Category
from decimal import Decimal


class HomePageView(generic.ListView):
    template_name = "home.html"
    paginate_by = 6
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['sizes'] = ['XS', 'S', 'M', 'L', 'XL']
        return context

    def get_queryset(self) -> QuerySet[Product]:
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset: QuerySet[Product]) -> List[Product]:
        filter_queries = self.request.GET.dict()

        if filter_queries.get('category') != None:
            if len(filter_queries.get('category')) < 10:
                queryset = queryset.filter(
                    category=filter_queries.get('category'))

        if filter_queries.get('promotion'):
            queryset = queryset.filter(promotion__isnull=False)

        queryset = self.filter_price(queryset, filter_queries)

        if filter_queries.get('size'):
            queryset = self.filter_sizes(queryset, filter_queries)

        return queryset

    def filter_price(self, queryset: QuerySet[Product], filter_queries: Dict[str, str]) -> QuerySet[Product]:
        if filter_queries.get('min-price'):
            queryset = queryset.filter(
                price__gte=Decimal(filter_queries.get('min-price').replace(',', '.')))
        if filter_queries.get('max-price'):
            queryset = queryset.filter(
                price__lte=Decimal(filter_queries.get('max-price').replace(',', '.')))
        return queryset

    def filter_sizes(self, queryset: QuerySet[Product], filter_queries: Dict[str, str]) -> List[Product]:
        products = []
        for product in queryset:
            if product.sizes.get_size_quantity(filter_queries.get('size')) > 0:
                products.append(product)
        return products
