from django.urls import path

from .views import ListView

urlpatterns = [
        path("/goods_list", ListView.as_view())
        ]
