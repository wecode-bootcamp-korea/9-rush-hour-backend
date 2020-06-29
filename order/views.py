import json

from django.http    import JsonResponse
from django.views   import View

from order.models   import Shipping

class ShippingManagementView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        try:
            Shipping(
                    shipping_name   = data['name'],
                    receiver        = data['recipient'],
                    address         = data['address'],
                    phone_number    = data['phone_number']
                    ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({'message': e + 'Invalid key.'})

    def get(self, request):
        shipping_list = Shipping.objects.values()
        return JsonResponse({'comments':list(shipping_list)}, status=200)
