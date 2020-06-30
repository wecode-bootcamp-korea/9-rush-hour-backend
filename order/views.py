import json
import uuid
from datetime import datetime

from django.views         import View
from django.http          import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#from user.utils             import login_decorator

from order.models           import * 
from product.models         import * 

class OrderView(View):
    #@login_decorator
    def get(self, request):
        
        # bringing the user_id
#        access_token = request.headers.get('Authorization')
#        decoded_token = jwt.decode(access_token, 'secret', algorithm='HS256')
#        decoded_user_id = decoded_token['id']
        
        user = UserInfo.objects.get(id=request.body.get('user_id'))

        # displaying user info
        user_info = {
            "name"         : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            "email"        : user.email
            }
        
        # shipping info - default shipping address
        shipping_method = request.body.get('shipping_method')
        if shipping_method == 'default':
            default_shipping = Shipping.objects.filter(basic=True).get(user_id=request.body.get('user_id'))

            shipping_info = {
                "recipient"    : default_shipping.recipient,
                "address"      : default_shipping.address,
                "phone_number" : default_shipping.phone_no
                }

        # shipping info - same as the user_info
        elif shipping_method == 'same_user':
            shipping_info = {
                "recipient"    : user.name,
                "address"      : user.address,
                "phone_number" : user.phone_number,
                }

        return JsonResponse({
            "user_info"       : list(user_info),
            "shipping_info"   : list(shipping_info),
            "payment_method"  : list(Payment.objects.values('name')), # payment method
            }, status=200)

    #@login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            # bringing the user_id
#            access_token = request.headers.get('Authorization')
#            decoded_token = jwt.decode(access_token, 'secret', algorithm='HS256')
#            user_id = decoded_token['id']
            
            # product info
            random_order_no = "lush_"+uuid.uuid4().hex+"_"+datetime.strftime(datetime.today(),"%Y%m%d") 

            order = Order.objects.create(user_info_id=data['user_id'], order_no=random_order_no, price=data['total_price'], payment_id=data['payment_id'], order_status_id=1, shipping_id=1)
            
            product_id_list = request.body.get('product_number')
            for i in product_id_list:
                OrderItem.objects.create(order=order, product=Product.objects.get(product_number=i))

            # shipping info - 직접입력
            ShippingInfo(
                name = data["name"],
                address = data["address"],
                phone_no = data["phone_no"],
                message = data["message"]
            ).save() 

        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER"}, status = 400)
