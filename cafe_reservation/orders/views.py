from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from django_filters.rest_framework import DjangoFilterBackend

from orders.models import Order
from orders. serializers import (
    OrderCreateSerializer,
    OrderGetSerialzier,
    OrderUpdateSerializer
)


class OrderViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания и просмотра заказа"""
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("table_number", "status")
    filterset_fields = ("status", )

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return OrderGetSerialzier
        elif self.action in ["update", "partial_update"]:
            return OrderUpdateSerializer
        return OrderCreateSerializer

    def get_object(self):
        order_id = self.kwargs['pk']
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise NotFound(
                detail=f"Заказа с id {self.kwargs['pk']} не существует"
            )
        return order
