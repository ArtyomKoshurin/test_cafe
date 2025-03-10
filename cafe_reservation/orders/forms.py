from django import forms

from api.models import Dish, Order
from api.constants import ORDER_STATUSES


class OrderCreateForm(forms.Form):
    """Форма для создания заказа."""
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

    def __init__(self, *args, **kwargs):
        """Отображение стоимости блюда рядом с его названием."""
        super().__init__(*args, **kwargs)
        self.fields['items'].label_from_instance = lambda dish: f"{dish.name}: {dish.price} руб."


class OrderStatusForm(forms.ModelForm):
    """Форма для смены статуса заказа."""
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                choices=ORDER_STATUSES,
                attrs={"class": "form-select"})
        }


class OrderItemsForm(forms.ModelForm):
    """Форма для редактирования состава блюд в заказе."""
    items = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Выберите блюда"
    )

    class Meta:
        model = Order
        fields = ['items']

    def __init__(self, *args, **kwargs):
        """Отображение стоимости блюда рядом с его названием."""
        super().__init__(*args, **kwargs)
        self.fields['items'].label_from_instance = lambda dish: f"{dish.name}: {dish.price} руб."
