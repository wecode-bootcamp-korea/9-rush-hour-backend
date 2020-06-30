from django.urls import path, include

urlpatterns = [
    path('mypage',include('order.urls')),
]
