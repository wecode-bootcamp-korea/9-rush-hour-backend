import json

from django.views         import View
from django.http          import JsonResponse, HttpResponse
from django.core.exceptions import ObjectDoesNotExist

#from user.utils             import login_decorator

from order.models           import * 
from product.models         import * 

#class CartView(View):
#    @login_decorator
#    def post(self, request, order_id):
#        try:
#            data = json.loads(request.body)
#
##            cart = OrderItem.objects.filter(order_id = request.order_id)
##            order_item   = Order.objects.filter(user_info = request.user_info)   
##            product = Product.objects.filter(product = request.product)
##            order_product = Order.objects.filter(product = request.product)
##            product_info = order_product.select_related('product_number')
#
#            #user_order = Order.objects.filter(user_info = request.user_info, order_no = data['order_no'])
#            user_products = Order.objects.select_related('ordered').prefetch_related('product').all()
#
#            OrderItem(
#                order = user_order.get(),
#                product = data['product_number']
#            ).save()
#                        
#            return HttpResponse(status = 200)
#            
#        except KeyError:
#            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)
#
#    def delete(self, request):
#        @login_check
#        cart = OrderItem.objects.filter(order = request.order)
#
#        if cart.exists():
#            cart.get().delete()
#            return HttpResponse(status=200)

class OrderView(View):
    #@login_decorator
    def get(self, request):
        
        # bringing the certain user
        access_token = request.headers.get('Authorization')
        decoded_token = jwt.decode(access_token, 'secret', algorithm='HS256')
        user_id = decoded_token['id']
        
        user = UserInfo.objects.get(id=user_id)

        # displaying user info
        user_info = {
            "name"         : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            "email"        : user.email
            }
        
        # shipping info - 기본 배송지
       


        # shipping info - 주문자정보와 동일
        shipping_info = {
            "recipient"    : user.name,
            "address"      : user.address,
            "phone_number" : user.phone_number,
            }

        return JsonResponse({
            "user_info"     : list(user_info),
            "shipping_info" : list(shipping_info),
            }, status=200)

    #@login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)

            #  shipping method
             

            # product info
            order = Order.objects.all()
            product_list = order.product.name.all()

            product_list = Order.objects.filter('product').all()
            for product in product_list:
                Order(
                    product_id = product.product_number,
                    amount = data['amount'],
                ).save()

            # payment options
            Payment(
                payment_name = data["name"]
            ).save()

            # shipping message
            Order(
                message = data['message']
            ).save()

        except Order.DoesNotExist:
            return JsonResponse({"message": "INVALID_ORDER"}, status = 400)
