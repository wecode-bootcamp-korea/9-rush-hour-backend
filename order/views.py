import json

from django.http    import JsonResponse
from django.views   import View

from order.models   import Shipping

class ShippingManagementView(View):
   # @login_decorator
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
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message': 'Invalid key.'})

    def get(self, request):
        shipping_list = Shipping.objects.values()
        return JsonResponse({'comments':list(shipping_list)}, status=200)

    def delete(self, request):
        data = json.loads(request.body)
        shipping_delete = Shipping.objects.get(id = data['user_id'])
        shipping_delete.delete()
        return JsonResponse({'message':'DELETE SUCCESS'}, status=200)
    
    def update(self,request):
        data = json.loads(request.body)
        shipping_update = Shipping.objects.get(id = data['user_id'])
        try:
            Shipping(
                    user_id      = data['user_id'],
                    name         = data['name'],
                    recipient    = data['recipient'],
                    address      = data['address'],
                    phone_number = data['phone_number']
                    ). ()
            return JsonResponse({'message':'SUCCESS UPDATE'}, status=200)
        except KeyError:
            return JsonResponse({'message': 'Invalid key.'})
