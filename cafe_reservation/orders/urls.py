from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders.views import OrderViewSet, EarningForDay

app_name = "orders"

router_orders = DefaultRouter()

router_orders.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router_orders.urls)),
    path('earnings/', EarningForDay.as_view())
]
