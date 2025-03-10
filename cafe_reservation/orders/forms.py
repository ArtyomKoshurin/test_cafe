from django import forms

from api.models import Dish


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
