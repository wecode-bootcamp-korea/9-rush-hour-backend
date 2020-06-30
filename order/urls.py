from django.urls import include, path
from .views  import OrderView 

urlpatterns = [
     path('', OrderView.as_view()),
     ]
