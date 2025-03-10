from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from orders.views import (
    OrderCreateView,
    OrderListView,
    OrderDetailView
)


app_name = "orders"

urlpatterns = [
    path('create-order/', OrderCreateView.as_view(), name='create_order'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path(
        'orders/<int:order_id>/',
        OrderDetailView.as_view(),
        name='order_detail'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
