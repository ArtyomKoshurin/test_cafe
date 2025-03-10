from django.db import models

from api.constants import ORDER_STATUSES


class Dish(models.Model):
    """Модель блюд."""
    name = models.CharField(max_length=64)
    price = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'price'],
                name='unique_name_price'
            )
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    """Модель заказа."""
    table_number = models.PositiveIntegerField()
    items = models.ManyToManyField(
        Dish,
        through='DishesForOrder',
        related_name='order_items'
    )
    total_price = models.IntegerField()
    status = models.CharField(
        max_length=16,
        choices=ORDER_STATUSES,
        default=ORDER_STATUSES[0][1]
    )

    def __str__(self):
        return f"table {self.table_number} is {self.status}"


class DishesForOrder(models.Model):
    """Вспомогательная модель связки блюд для заказа."""
    order = models.ForeignKey(
        Order,
        related_name='dish_for_order',
        on_delete=models.CASCADE
    )
    dish = models.ForeignKey(
        Dish,
        related_name='dish_for_order',
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['order', 'dish'],
                name='unique_dish_order'
            )
        ]

    def __str__(self):
        return f'{self.order}: {self.dish}'
