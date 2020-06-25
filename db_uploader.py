import os
import django
import csv
import sys
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lush.settings")
django.setup()

from product.models import *
from order.models import *

CSV_PATH = "./Lush_FINAL.csv"

with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    
    # Menu
    menu_list = ["제품","브랜드","매장안내","스파","이벤트"]
    for i in menu_list:
        Menu.objects.create(name = i)

    # Category
    category_list = {
        "001013" :  "베스트"   ,
        "001011" :  "신제품"   ,
        "001001" :  "배쓰"     ,
        "001002" :  "샤워"     ,
        "001003" :  "보디"     ,
        "001005" :  "페이스"   ,
        "001004" :  "헤어"     ,
        "001006" :  "메이크업" ,
        "001007" :  "퍼퓸"     ,
        "001009" :  "기프트"   ,
            }
    for key,value in category_list.items():
        menu_id = Menu.objects.get(id=1).id
        Category.objects.create(name = value, code = key, menu_id = menu_id)

    # Subcategory
    subcategory_list = {
        "001013001" :   "주간 베스트"    ,
        "001013002" :   "별 다섯개 후기" ,
        "001013005" :   "온라인 전용"    ,
        "001013006" :   "국내제조"       ,
        "001013009" :   "네이키드"       ,
        "001013011" :   "환상의 짝꿍"    ,
        "001011040" :   "보디 스프레이"  ,
        "001011002" :   "버블 바 큐래이션",
        "001011039" :   "스프링 컬렉션"  ,
        "001011045" :   "마더스&파더스"  ,
        "001001001" :   "배쓰 밤"        ,
        "001001002" :   "버블 바"        ,
        "001001003" :   "배쓰 오일"      ,
        "001001004" :   "펀"             ,
        "001001005" :   "젤리 밤"        ,
        "001002001" :   "솝"             ,
        "001002002" :   "샤워 젤 & 젤리" ,
        "001002003" :   "보디 컨디셔너"  ,
        "001002009" :   "샤워 오일"      ,
        "001002008" :   "샤워 밤"        ,
        "001002004" :   "스크럽 & 버터"  ,
        "001002006" :   "펀"             ,
        "001003001" :   "클렌저"         ,
        "001003002" :   "로션"           ,
        "001003003" :   "핸드 앤 풋"     ,
        "001003004" :   "마사지 바"      ,
        "001003006" :   "더스팅 파우더"  ,
        "001003010" :   "쉐이빙 크림"    ,
        "001005001" :   "클렌저"         ,
        "001005004" :   "페이스 마스크"  ,
        "001005002" :   "토너"           ,
        "001005003" :   "모이스춰라이저" ,
        "001005007" :   "프라이머"       ,
        "001005005" :   "립"             ,
        "001005006" :   "쉐이빙 크림"    ,
        "001004001" :   "샴푸 바"        ,
        "001004002" :   "샴푸"           ,
        "001004003" :   "드라이 샴푸"    ,
        "001004004" :   "컨디셔너"       ,
        "001004005" :   "트리트먼트"     ,
        "001004006" :   "스타일링"       ,
        "001006001" :   "페이스 파우더"  ,
        "001006002" :   "아이 메이크업"  ,
        "001006007" :   "파운데이션"     ,
        "001006009" :   "스킨 틴트"      ,
        "001006010" :   "비건 브러쉬"    ,
        "001007011" :   "보디 스프레이"  ,
        "001007001" :   "퍼퓸 라이브러리",
        "001007002" :   "코어 레인지"    ,
        "001007008" :   "솔리드 퍼퓸"    ,
        "001007009" :   "워시 카드"      ,
        "001007010" :   "퍼퓸 낫랩"      ,
        "001009016" :   "기프트 베스트"  ,
        "001009013" :   "1-3만원대"      ,
        "001009014" :   "4-6만원대"      ,
        "001009015" :   "7만원 이상"     ,
        "001009010" :   "낫랩"           ,
        "001009012" :   "스웨그"         ,
        "001009003" :   "악세사리"       ,
            } 
    for i in list(category_list.keys()):
        for key,value in subcategory_list.items():
            if key.startswith(i):
                category_id = Category.objects.get(code = i).id
                global sub_category
                sub_category = SubCategory.objects.create(name = value, code = key, category_id = category_id)
            else:
                continue

    for row in data_reader:
        # Detail
        video_url    = row[10]
        html         = row[11]
        detail = Detail.objects.create(video_url = video_url, html = html)

        if row[5] == "TRUE":
            row[5] = True
        else:
            row[5] = False

        if row[6] == "TRUE":
            row[6] = True
        else:
            row[6] = False

        if row[7] == "TRUE":
            row[7] = True
        else:
            row[7] = False

        # Product
        product_no   = row[4]
        name         = row[1]
        is_new       = row[7]
        is_vegan     = row[6]
        price        = row[3]
        hash_tag     = row[2]
        if row[5] == True:
            stock = 0
        else :
            stock = random.randint(1,10)
        
        product = Product.objects.create(
                product_no      = product_no,
                name            = name,
                is_new          = is_new,
                is_vegan        = is_vegan,
                hash_tag        = hash_tag,
                price           = price,
                stock           = stock,
                sub_category    = sub_category,
                detail          = detail
                )

        # Image
        url = row[8].split
        Image.objects.create(url = url, product = product)

        # Weight
        weight_g     = row[9]
        extra_price  = 0
        Weight.objects.create(weight_g = weight_g, extra_price = extra_price, product = product)

with open(CSV_PATH) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        # RelatedProduct
        rand_list = []
        for i in range(3):
            random_product = random.choice(Product.objects.exclude(product_no = row[4])).id
            if not RelatedProduct.objects.filter(to_product_id = random_product).exists():
                rand_list.append(random.choice(Product.objects.exclude(product_no = row[4])))
            else:
                if random_product == 83:
                    random_product -= 1
                    rand_list.append(Product.objects.get(id = random_product))
                else:
                    random_product += 1
                    rand_list.append(Product.objects.get(id = random_product))
        #rand_list = [random.choice(Product.objects.exclude(product_no = row[4])) for i in range(2)]
        from_product = Product.objects.get(product_no = row[4])
        for to_product in rand_list:
            RelatedProduct.objects.create(from_product = from_product, to_product = to_product)
    
    # Payment
    payment_lists = ["신용카드","계좌이체","가상계좌","휴대폰결제","페이코"]
    for i in payment_lists:
        Payment.objects.create(payment = i)

    # OrderStatus
    order_status_lists = [
            "주문 접수",
            "입금 확인",
            "출고 처리 중",
            "출고 완료",
            "배송 시작",
            "배송 완료",
            "구매 확정",
            "주문 취소",
            "교환 요청",
            "교환 접수",
            "교환 완료",
            "환불 요청",
            "환불 접수",
            "환불 완료",
            ]
    for i in order_status_lists:
        OrderStatus.objects.create(status = i)
