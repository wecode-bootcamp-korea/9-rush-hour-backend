from django.urls import (
    include, 
    path
)

from .views      import (
    OrderView,
    PayView
)

urlpatterns = [
     path('/order', OrderView.as_view()),
     path('/pay', PayView.as_view())
]
