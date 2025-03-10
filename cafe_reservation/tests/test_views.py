import pytest

from django.urls import reverse
from django.test import Client
from unittest.mock import patch

from api.models import Order, Dish


order_for_view = {
    "id": 1,
    "table_number": 5,
    "items": [],
    "total_price": 100,
    "status": "Paid"
}


@pytest.mark.django_db
class TestOrderViews:

    def setup_method(self):
        self.client = Client()

    @patch("requests.get")
    def test_order_list_view(self, mock_get):
        """Тест отображения списка заказов."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [order_for_view]

        response = self.client.get(reverse("orders:orders_list"))
        assert response.status_code == 200
        assert "Список заказов" in response.content.decode()

    @patch("requests.post")
    def test_order_create_view(self, mock_post):
        """Тест создания заказа."""
        dish = Dish.objects.create(name="Пицца", price=500)
        data = {"table_number": 3, "items": [dish.id]}

        mock_post.return_value.status_code = 201

        response = self.client.post(reverse("orders:create_order"), data)
        assert response.status_code == 302
        assert response.url == reverse("orders:orders_list")

    @patch("requests.get")
    @patch("requests.patch")
    def test_edit_order_items_view(self, mock_patch, mock_get):
        """Тест редактирования состава блюд в заказе."""
        dish1 = Dish.objects.create(name="Паста", price=400)
        dish2 = Dish.objects.create(name="Салат", price=250)
        order = Order.objects.create(table_number=2, status="Waiting")
        order.items.add(dish1)

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": order.id,
            "table_number": order.table_number,
            "items": [
                {
                    "id": dish1.id,
                    "name": dish1.name,
                    "price": dish1.price
                }
            ],
            "status": order.status
        }

        data = {"items": [dish2.id]}
        mock_patch.return_value.status_code = 200

        response = self.client.post(
            reverse("orders:edit_order_items", args=[order.id]), data
        )
        assert response.status_code == 302
        assert response.url == reverse("orders:order_detail", args=[order.id])
