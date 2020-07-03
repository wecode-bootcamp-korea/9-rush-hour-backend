import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import (
    Count, 
    F 
)

from .models            import (
    Product, 
    Category, 
    SubCategory,
    Spa,
    Store
)
from lush_settings      import LIST_COUNT
        
def make_product_list(lists):
    product_list = [
        {
        "product_name"      : product.name,
        "product_number"    : product.product_number,
        "is_new"            : product.is_new,
        "is_vegan"          : product.is_vegan,
        "hash_tag"          : product.hash_tag,
        "price"             : int(product.price),
        "stock"             : product.stock,
        "image"             : product.thumbnail_image.first().url,
        "sub_category_name" : product.sub_category.name,
        "sub_category_code" : product.sub_category.code
        }
        for product in lists
    ]
    return product_list

class ProductListView(View):
    def get(self, request):
        try:
            page                = int(request.GET.get("page",1))
            category_code       = request.GET.get("categoryCode")
            sub_category_code   = request.GET.get("subCategoryCode")
            product_count       = LIST_COUNT
            limit               = product_count * page
            offset              = limit - product_count
    
             # Category 기준 카운트
            total_category  = Product.objects.values(
                "sub_category__category__name",
                "sub_category__category__code",
            ).annotate(
                category_name = F("sub_category__category__name"),
                category_code = F("sub_category__category__code"),
                total = Count("category_name"),
            )
            # Sub_category 기준 카운트            
            total_sub_category = Product.objects.values(
                "sub_category__name",
                "sub_category__code",
            ).annotate(
                category_name = F("sub_category__name"),
                category_code = F("sub_category__code"),
                total = Count("category_name")
            ) 
            
            # Category or Sub_category filtering
            if category_code:
                filters = {"sub_category__category__code":category_code}
            if sub_category_code:
                filters = {"sub_category__code":sub_category_code}
            if Product.objects.filter(**filters).exists():
                all_products = Product.objects.prefetch_related(
                    "thumbnail_image"
                ).select_related(
                    "sub_category"
                ).filter(**filters).order_by("-is_new")[offset:limit]
                product_list = make_product_list(all_products)
                return JsonResponse(
                    {
                        "product":product_list,
                        "count"  :list(total_category)+list(total_sub_category)
                    },
                    status=200
                )

            return JsonResponse({"message":"PRODUCT DOES NOT EXIST"}, status=404)
        
        except KeyError as e:
            return JsonResponse({"message":f"{e} KEY ERROR"}, status = 400)

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            if Product.objects.filter(product_number = product_id).exists():
                product_detail = Product.objects.filter(
                    product_number=product_id
                ).prefetch_related(
                    "thumbnail_image",
                    "weight",
                    "related_products"
                ).select_related(
                    "detail"
                ).first()

                detail_info ={
                    "product_name"  : product_detail.name,
                    "hash_tag"      : product_detail.hash_tag,
                    "image"         : product_detail.thumbnail_image.first().url,
                    "price"         : int(product_detail.price),
                    "weight"        : product_detail.weight.first().weight_g,
                    "extra_price"   : int(product_detail.weight.first().extra_price),
                    "video"         : product_detail.detail.video_url,
                    "html"          : product_detail.detail.html,
                    "related"       : make_product_list([product.to_product for product in product_detail.to_product.all()])
                }
                
                return JsonResponse(
                    {
                    "detail":detail_info,
                    },
                    status=200
                )
            return JsonResponse({"message":"PRODUCT DOES NOT EXIST"}, status=404)
        
        except KeyError as e:
            return JsonResponse({"message":f"{e} KEY ERROR"}, status = 400)

class SpaView(View):
    def get(self,request):
        spa = Spa.objects.all()
        spa_list = [
                {
                    'name'      : spa_info.name,
                    'hashtag'   : spa_info.hashtag,
                    'url'       : spa_info.url,
                    'price'     : spa_info.price
                } for spa_info in spa 
            ]

        return JsonResponse({"spa_list":spa_list})

class StoreView(View):
    def get(self,request):
        store = Store.objects.all()
        store_list = [
                {
                    'name'  : store_info.name,
                    'url'   : store_info.url
                } for store_info in store 
            ]

        return JsonResponse({"store_list":store_list})

