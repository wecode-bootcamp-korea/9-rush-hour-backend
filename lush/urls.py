from django.urls import path,include

urlpatterns = [
        path("goods", include("product.urls")),
        path("user", include("user.urls")),
        path("order", include("order.urls"))
]
