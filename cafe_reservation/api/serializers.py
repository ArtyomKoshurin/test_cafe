from rest_framework import serializers

from api.models import Dish, Order, DishesForOrder
from api.constants import ORDER_STATUSES


class DishSerialzier(serializers.Serializer):
    """Сериализатор для отображения информации о блюдах."""

    name = serializers.CharField(max_length=64)
    price = serializers.IntegerField()


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказов."""

    table_number = serializers.IntegerField()
    items = DishSerialzier(many=True)
    total_price = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "table_number", "items", "total_price", "status")

    def validate_table_number(self, value):
        if value < 1 or value > 30:
            raise serializers.ValidationError(
                "Стола с таким номером не существует."
            )

        return value

    def validate(self, data):
        items = data.get('items')
        if not items:
            raise serializers.ValidationError(
                "Необходимо добавить блюда в заказ."
            )
        for dish in items:
            name = dish.get("name")
            price = dish.get("price")
            if not Dish.objects.filter(name=name, price=price).exists():
                raise serializers.ValidationError(
                    f"Блюда {name} с ценой {price} у нас в продаже нет."
                )

        return data

    def create(self, validated_data):
        items = validated_data.pop("items")
        total_price = sum(dish.get("price") for dish in items)

        order = Order.objects.create(
            table_number=validated_data.get("table_number"),
            total_price=total_price,
            status=ORDER_STATUSES[0][1]
        )

        for dish in items:
            dish = Dish.objects.get(
                name=dish.get("name"),
                price=dish.get("price")
            )
            DishesForOrder.objects.create(
                dish=dish,
                order=order
            )

        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления заказов."""

    table_number = serializers.IntegerField(required=False)
    items = DishSerialzier(many=True, required=False)
    total_price = serializers.IntegerField(read_only=True)
    status = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = ("id", "table_number", "items", "total_price", "status")

    def validate(self, data):
        if "items" in data:
            items = data.get('items')
            if not items:
                raise serializers.ValidationError(
                    "Необходимо добавить блюда в заказ."
                    )
            for dish in items:
                name = dish.get("name")
                price = dish.get("price")
                if not Dish.objects.filter(name=name, price=price).exists():
                    raise serializers.ValidationError(
                        f"Блюда {name} с ценой {price} у нас в продаже нет."
                    )
        if "status" in data:
            status = data.get("status")
            if not status or status not in ["Waiting", "Ready", "Paid"]:
                raise serializers.ValidationError(
                    "Укажите корректный статус для изменения заказа."
                )

        return data

    def update(self, instance, validated_data):

        if "items" in validated_data:
            items = validated_data.pop("items")
            total_price = sum(dish.get("price") for dish in items)

            instance.items.clear()
            for dish in items:
                dish = Dish.objects.get(
                    name=dish.get("name"),
                    price=dish.get("price")
                )
                DishesForOrder.objects.create(dish=dish, order=instance)
            instance.total_price = total_price

        if "status" in validated_data:
            instance.status = validated_data.get("status", instance.status)

        instance.save()
        return instance


class OrderGetSerialzier(serializers.ModelSerializer):
    """Сериализатор для получения информации о заказе."""

    items = DishSerialzier(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "table_number", "items", "total_price", "status")
