import json

import django.views import View
import django.http  import JsonResponse, HttpResponse

#from user.utils     import login_decorator

from order.models   import (
    Order,
    Payment
)

from product.models import Image

class PaymentView(View):
    def post(self, request):
        data = json.loads(request.body)

        Payment(
            payment_name = data["name"]
        ).save()

        return JsonResponse({"payment method": list(Payment)}, status=200)

#    def get(self, request, payment_name):
#        return JsonResponse({'Payment Method': Payment.objects.filter(name=payment_name)}, status=200)

#class OrderStatusView(View):
#    def get(self, request):
#        return JsonResponse({'Order Status': OrderStatus.objects.filter(status=request.status), status=200)

class UserInfoView(View):

    #여기의 user_id는 어디서 오는가? 이 user_id는 유저 고유의 id?
    def get(self, request, user_id):       

         # 여기서 클래스의 related_name 사용?? or 그냥 user_info? 그리고 user_id가 같은 유저를 가져오는게 맞는지 not sure??
        user_info_list = Order.objects.select_related('user_info').filter(user_id=user_id)         
        user_info = [{
            "name"         : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            "email"        : user.email
            } for user in user_info_list]  # 유저 한명마다 리턴

        return JsonResponse({"user_info": user_info}, status=200)

class ProductView(View):
    # 데코레이터 필요한가? 애초에 로그인을 안하면 장바구니로 못들어가서 probably not
    def get(self, request):
        product_list = Order.objects.prefetch_related('product')
        product_info = [{
            "image" : Image.url,  # 수정!!
            "name" : product_list.name,
            "subcateogry" : product_list.sub_category,
            "price" : product_list.price
            } for product in product_list]

        return JsonResponse({"product_info" : product_info}, status=200})

class ShippingView(View):
    def post(self, request):
        data = json.loads(request.body)
        
        # shipping message
        Order(
            message = data['message']
        ).save()
        return JsonResponse({"message" : list(Order)}, status=200) 

    def get(self, request):

