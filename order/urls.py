from django.urls import path

from order.views import ShippingManagementView, OrderView, PayView

urlpatterns = [
        path('/shipping', ShippingManagementView.as_view()),
        path('/shipping/<int:shipping_id>', ShippingManagementView.as_view()),
        path('/order', OrderView.as_view()),
        path('/pay', PayView.as_view())
]
