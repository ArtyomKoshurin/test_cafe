from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum

from api.models import Order
from api. serializers import (
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


class EarningForDay(APIView):
    """Вью класс для подсчета общей выручки."""

    def get(self, request):
        # В ТЗ об этом не было сказано, но я бы добавил возможность выставлять
        # дату создания заказа, чтобы считать не общую выручку со всех заказов
        # (как в реализации ниже), а за конкретный день (datetime.now().date())
        total_earning = Order.objects.aggregate(
            total_earning=Sum("total_price")
        ).get("total_earning")

        if not total_earning:
            total_earning = 0

        return Response(f"Общая выручка за смену: {total_earning} руб.")
