from typing import Any
from django import forms
from store.models import Order, Shipping, OrderData


class OrderForm(forms.ModelForm):

    street1 = forms.CharField(max_length=120)
    street2 = forms.CharField(max_length=120)
    country = forms.CharField(max_length=120)
    zip_code = forms.CharField(max_length=10)

    class Meta:
        model = OrderData
        fields = '__all__'

    def __init__(self, total_price, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.total_price = total_price

    def save(self, commit: bool = True) -> Order:
        instance = super().save(commit=False)
        form_data = self.cleaned_data
        shipping_data = Shipping.objects.create(
            street1=form_data.pop('street1'),
            street2=form_data.pop('street2'),
            country=form_data.pop('country'),
            zip_code=form_data.pop('zip_code')
        )

        if commit:
            instance.save()
            order = Order.objects.create(
                order_data=instance,
                shipping=shipping_data,
                total=self.total_price
            )

        return order
