from django import forms

from api.models import Dish, Order
from api.constants import ORDER_STATUSES


class OrderForm(forms.Form):
    table_number = forms.IntegerField(
        min_value=1,
        max_value=30,
        label="Номер стола"
    )
    items = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда"
    )


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                choices=ORDER_STATUSES,
                attrs={"class": "form-select"})
        }
