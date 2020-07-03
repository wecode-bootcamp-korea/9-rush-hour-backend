from django.urls import path

from .views import (
    ProductListView,
    ProductDetailView,
    SpaView,
    StoreView
)

urlpatterns = [
    path("", ProductListView.as_view()),
    path("/<slug:product_id>", ProductDetailView.as_view()),
]
