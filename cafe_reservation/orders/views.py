import requests

from django.shortcuts import render, redirect
from django.views import View

from orders.forms import OrderForm


class OrderCreateView(View):
    template_name = "order_create.html"

    def get(self, request):
        form = OrderForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            table_number = form.cleaned_data["table_number"]
            items = form.cleaned_data["items"]

            items_data = [{"name": dish.name, "price": dish.price} for dish in items]

            response = requests.post(
                "http://127.0.0.1:8000/api/orders/",
                json={"table_number": table_number, "items": items_data},
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 201:
                return redirect("success_page")

        return render(request, self.template_name, {"form": form})
