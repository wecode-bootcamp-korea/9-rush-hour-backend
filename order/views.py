import json

from django.http    import JsonResponse
from django.views   import View

from .models        import *

class ShippingManagementView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            Shipping(
                    user_id         = data['user_id'],
                    name            = data['name'],
                    recipient       = data['recipient'],
                    address         = data['address'],
                    phone_number    = data['phone_number']
                    ).save()
            return JsonResponse({'message':'SUCCESS POST'}, status=200)

        except KeyError as e:
            return JsonResponse({'message': 'Invalid key.'.e}, status = 401)

    def get(self, request):
        shipping_list = Shipping.objects.values()
        return JsonResponse({'comments':list(shipping_list)}, status=200)

    def delete(self, request):
        data            = json.loads(request.body)
        shipping_delete = Shipping.objects.get(id = data['id'])
        shipping_delete.delete()
        return JsonResponse({'message':'DELETE SUCCESS'}, status=200)
    
    def put(self,request):
        data            = json.loads(request.body)
        name            = data['name']
        shipping_update = Shipping.objects.get(id = data['id'])
        try:
            shipping_update.name         = data['name']
            shipping_update.address      = data['address']
            shipping_update.recipient    = data['recipient']
            shipping_update.phone_number = data['phone_number']
            shipping_update.save()  
            return JsonResponse({'message':'SUCCESS UPDATE'}, status=200)

        except KeyError as e:
            return JsonResponse({'message': 'Invalid key.'.e}, status = 401)
