from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from orders.views import OrderCreateView


urlpatterns = [
    path('create-order/', OrderCreateView.as_view(), name='create_order'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )
