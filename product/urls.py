from django.urls import path

from .views import ProductListView

urlpatterns = [
        path("/goods_list", ProductListView.as_view())
        ]
