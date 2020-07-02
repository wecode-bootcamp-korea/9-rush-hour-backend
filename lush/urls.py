from django.urls import path, include

urlpatterns = [
    path('mypage',  include('order.urls')),
    path("goods" ,  include("product.urls")),
    path("user"  ,  include("user.urls")),
    path("review",  include("review.urls")),
    
]
