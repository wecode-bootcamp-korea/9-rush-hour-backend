from django.http                    import HttpResponse, JsonResponse
from django.views                   import View
from django.db.models               import Count, F

import json

from .models          import Product, Category, SubCategory

class ListView(View):
    def get(self, request):
        page = int(request.GET.get("page",1))
        category_code = request.GET.get("cateCd")
        
        list_count = 28
        limit = list_count * page
        offset = limit - list_count
        all_products = Product.objects.all().prefetch_related(
                "thumbnail_image"
                ).select_related(
                        "sub_category"
                        )[offset:limit]

         # Category 기준 카운트
        rename_list = Product.objects.annotate(
                category_name = F("sub_category__category__name"),
                category_code = F("sub_category__category__code"),
                )
        total_ctgry = rename_list.values(
                "category_name",
                "category_code"
                ).annotate(
                        total = Count("category_name")
                        )
        # Sub_category 기준 카운트            
        rename_sub_list = Product.objects.annotate(
                category_name = F("sub_category__name"),
                category_code = F("sub_category__code")
                )
        total_sub_ctgry = rename_sub_list.values(
                "category_name",
                "category_code"
                ).annotate(
                        total = Count("category_name")
                        ) 
        
        def send_info(lists):
            product_list = []
            for product in lists:
                product_info = {}
                product_info["product_name"]   = product.name
                product_info["product_number"] = product.product_number
                product_info["is_new"]         = product.is_new
                product_info["is_vegan"]       = product.is_vegan
                product_info["hash_tag"]       = product.hash_tag
                product_info["price"]          = int(product.price)
                product_info["stock"]          = product.stock
                product_info["image"]          = product.thumbnail_image.all()[0].url
                product_info["sub_ctgry_name"] = product.sub_category.name
                product_info["sub_ctgry_code"] = product.sub_category.code
                product_list.append(product_info)
            return product_list

        try :
            # Category 전체 기준 리스트
            if Category.objects.filter(code = category_code).exists():
                all_products = Product.objects.all().prefetch_related(
                        "thumbnail_image"
                        ).select_related(
                                "sub_category"
                                )[offset:limit]
                product_list = send_info(all_products)
                return JsonResponse(
                        {
                            "product":product_list,
                            "count":list(total_ctgry)+list(total_sub_ctgry)
                            }, 
                        status=200
                        )
            else :
                # Sub_category 기준 리스트
                sub_category_products = Product.objects.filter(
                        sub_category__code = category_code
                        )[offset:limit]
                product_list = send_info(sub_category_products)

                return JsonResponse(
                        {
                            "product":product_list,
                            "count":list(total_ctgry)+list(total_sub_ctgry)
                            },
                        status = 200
                        )
        except:
            return HttpResponse(status=400)
