import json

import django.views import View
import django.http  import JsonResponse

from order.models   import *

class OrderView(View):
    def post(self, request):
        Order(
             payment = Payment.name,
        ).save()

    def get(self, request):
        payment_info = Payment.objects.values()
        Order_list = {}

        Order_list{


        #return JsonResponse({'Payment Method': payment_info}, status=200)
