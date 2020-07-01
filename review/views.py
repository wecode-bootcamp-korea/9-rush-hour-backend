import json

from django.http    import JsonResponse
from django.views   import View

from .models        import (
    Review,
    ReviewImage
)
from product.models import Product
from user.models    import UserInfo
from user.utils     import login_decorator

class ProductCommentView(View):
    def get(self, request, product_id):
        

    @login_decorator
    def post(self, request, product_id):
        data = json.loads(request.body)
        Review.objects.create(
            stars   = data["stars"],
            review  = data["review"],
            user_id = data["user"],
            product = Product.objects.get(product_number=product_id)
        )
        return JsonResponse({"message":"REVIEW ADDED"}, status=200)
