from django.urls import path
from .views      import ProductCommentView

urlpatterns = [
    path("/<slug:product_id>", ProductCommentView.as_view())
]
