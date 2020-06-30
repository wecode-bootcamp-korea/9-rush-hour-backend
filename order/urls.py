from django.urls import path

from order.views import ShippingManagementView

urlpatterns = [
        path('/shipping', ShippingManagementView.as_view())
]
