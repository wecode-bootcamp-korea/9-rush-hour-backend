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
    path("/spa", SpaView.as_view()),
    path("/store", StoreView.as_view())
]
