from django.urls import path

from .views import (
    LoginView, 
    SignUp
)

urlpatterns = [
        path('/signin', LoginView.as_view()),
        path('/signup',SignUp.as_view()),
]
