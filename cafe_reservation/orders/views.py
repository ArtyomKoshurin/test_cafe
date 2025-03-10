import requests

from django.shortcuts import render, redirect
from django.views import View

from orders.forms import OrderCreateForm, OrderStatusForm


class OrderListView(View):
    template_name = "orders_list.html"

    def get(self, request):
        table_number = request.GET.get("table_number", "").strip()
        status = request.GET.get("status", "").strip()

        params = {}
        if table_number:
            params["table_number"] = int(table_number)
        if status:
            params["status"] = status

        response = requests.get(
            "http://127.0.0.1:8000/api/orders/",
            params=params
        )
        orders = response.json() if response.status_code == 200 else []

        return render(request, self.template_name, {"orders": orders})


class OrderDetailView(View):
    template_name = "order_detail.html"

    def get(self, request, order_id):
        response = requests.get(
            f"http://127.0.0.1:8000/api/orders/{order_id}/"
        )
        if response.status_code == 200:
            order = response.json()
        else:
            order = None

        form = OrderStatusForm(
            initial={"status": order["status"]}
        ) if order else None
        return render(
            request,
            self.template_name,
            {"order": order, "form": form}
        )

    def post(self, request, order_id):
        form = OrderStatusForm(request.POST)
        if form.is_valid():
            new_status = form.cleaned_data["status"]
            requests.patch(
                f"http://127.0.0.1:8000/api/orders/{order_id}/",
                json={"status": new_status},
                headers={"Content-Type": "application/json"}
            )
        return redirect("orders:order_detail", order_id=order_id)


class OrderCreateView(View):
    template_name = "order_create.html"

    def get(self, request):
        form = OrderCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = OrderCreateForm(request.POST)
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
                return redirect("orders:orders_list")

        return render(request, self.template_name, {"form": form})


class OrderDeleteView(View):
    def post(self, request, order_id):
        requests.delete(f"http://127.0.0.1:8000/api/orders/{order_id}/")
        return redirect("orders:orders_list")
