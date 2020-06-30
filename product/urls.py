from django.urls import path

from .views import ProductListView, ProductDetailView

urlpatterns = [
        path("/goods_list", ProductListView.as_view()),
        path("/<slug:product_id>", ProductDetailView.as_view()),
        ]
