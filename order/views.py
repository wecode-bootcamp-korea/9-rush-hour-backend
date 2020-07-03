import json
import uuid
import jwt
from datetime import datetime

from django.http    import JsonResponse,HttpResponse
from django.views   import View
from django.core.exceptions import ObjectDoesNotExist

from order.models   import ShippingList, Order, OrderItem, ShippingInfo
from user.utils     import login_decorator
from user.models    import UserInfo
from product.models import Product

from lush.settings  import SECRET_KEY, ALGORITHMS

class ShippingManagementView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        print(data)
        try:
            ShippingList(
                        user_id         = data['user'],
                        name            = data['name'],
                        recipient       = data['recipient'],
                        address         = data['address'],
                        phone_number    = data['phone_number']
                    ).save()
            return HttpResponse(status=200)

        except KeyError :
            return JsonResponse({'message': 'INVALID_KEY.'}, status = 401)

    @login_decorator
    def get(self, request):
        data          = json.loads(request.body)
        user_id       = request.user.id
        shipping_list = ShippingList.objects.filter(user_id = user_id).values()
        return JsonResponse({'shipping':list(shipping_list)}, status=200)

    def delete(self, request, shipping_id):
        shipping_delete = ShippingList.objects.get(id = shipping_id)
        shipping_delete.delete()
        return JsonResponse({'message':'DELETE_SUCCESS'}, status=200)
    
    def put(self, request, shipping_id):
        data            = json.loads(request.body)
        shipping_update = ShippingList.objects.get(id = shipping_id)
        try:
            shipping_update.name         = data['name']
            shipping_update.address      = data['address']
            shipping_update.recipient    = data['recipient']
            shipping_update.phone_number = data['phone_number']
            shipping_update.save()  
            return JsonResponse({'message':'UPDATE_SUCCESS'}, status=200)

        except KeyError :
            return JsonResponse({'message': 'INVALID_KEY.'}, status = 400)

class OrderView(View):

    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            user_id = request.user.id 
            order = Order.objects.create(
                user_info_id    = user_id, 
                price           = data['price'], 
                order_status_id = 1
            )

            order_item = OrderItem.objects.create(
                order   = order,
                product = Product.objects.get(product_number = data['product_number']),
                amount  = data['amount']
            )
            
            return HttpResponse(status = 200) 
        
        except Product.DoesNotExist:
            return JsonResponse({"message": "PRODUCT_NOT_FOUND"}, status = 404) 
        
class PayView(View):

    @login_decorator
    def get(self, request):
        data = json.loads(request.body)
        
        user_id = request.user.id
        user = UserInfo.objects.get(id=user_id)

        user_info = {
            "name"         : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            "email"        : user.email
        }
        
        shipping_method = data['shipping_method']

        # shipping info - default shipping address (기본 배송지)
        if shipping_method == 'default':
            default_shipping = ShippingList.objects.filter(default=True).get(user_id=decoded_user_id)

            shipping_info = {
                "recipient"    : default_shipping.recipient,
                "address"      : default_shipping.address,
                "phone_number" : default_shipping.phone_no
            }

        # shipping info - same as the user_info (주문자정보와 동일)
        elif shipping_method == 'same_user':
            shipping_info = {
                "recipient"    : user.name,
                "address"      : user.address,
                "phone_number" : user.phone_number
            }
        
        # payment_method 
        payment = Order.objects.filter(user_info_id = decoded_user_id).values()[0]
        payment_method = {
            "payment_method" : payment['payment_id']
        }

        return JsonResponse(
            {
            "user_info"       : user_info,
            "shipping_info"   : shipping_info,
            "payment_method"  : payment_method
            }, 
            status=200 
        )
    
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = request.user.id

            # shipping info - 직접입력일때
            shipping_info = ShippingInfo.objects.create(
                name             = data["name"],
                address          = data["address"],
                phone_number     = data["phone_no"],
                message          = data["message"]
            )
            
            # generating a random order number
            random_order_no = "lush_"+uuid.uuid4().hex+"_"+datetime.strftime(datetime.today(),"%Y%m%d") 
            
            order = Order.objects.create(
                user_info_id    = user_id, 
                order_number    = random_order_no, 
                price           = data['price'], 
                payment_id      = data['payment_id'], 
                order_status_id = 2, 
                shipping        = shipping_info 
            )

            # saving product numbers
            product_id_list = data['product_number']
            for i in range(len(product_id_list)):
                OrderItem.objects.create(
                        order=order, 
                        product=Product.objects.get(product_number=product_id_list[i]), 
                        amount=data['product_amount'][i]
                )

            return HttpResponse(status = 200)

        except Order.DoesNotExist:
            return JsonResponse({"message": "ORDER_NOT_FOUND"}, status = 404)
