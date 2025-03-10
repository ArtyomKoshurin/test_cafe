from django.urls import path

from orders.views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView,
    OrderDeleteView,
    EarningsDetailView,
    EditOrderItemsView
)


app_name = "orders"

urlpatterns = [
    path('create-order/', OrderCreateView.as_view(), name='create_order'),
    path('', OrderListView.as_view(), name='orders_list'),
    path(
        '<int:order_id>/',
        OrderDetailView.as_view(),
        name='order_detail'
    ),
    path(
        '<int:order_id>/delete/',
        OrderDeleteView.as_view(),
        name='order_delete'
    ),
    path('earnings/', EarningsDetailView.as_view(), name='earnings_detail'),
    path(
        '<int:order_id>/edit-items/',
        EditOrderItemsView.as_view(),
        name='edit_order_items'
    )
]
