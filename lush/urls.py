from django.urls import path, include

urlpatterns = [
    path("goods/", include("product.urls"))
]
