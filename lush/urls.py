from django.urls import path, include
from product.views import SpaView, StoreView

urlpatterns = [
    path('mypage',  include('order.urls')),
    path("goods" ,  include("product.urls")),
    path("user"  ,  include("user.urls")),
    path("review",  include("review.urls")),
    path("spa", SpaView.as_view()),
    path("store", StoreView.as_view()), 
]
