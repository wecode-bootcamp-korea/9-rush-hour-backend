import requests
import csv
import time

from selenium import webdriver
from bs4 import BeautifulSoup

file_name = "lush_product_list.csv"
csv_open = open(file_name, "w+", encoding = "utf-8")
csv_writer = csv.writer(csv_open)
#csv_writer.writerow(("product_name", "video_url"))
csv_writer.writerow(

driver = webdriver.Chrome()

codes = ["001001001","001001002"]
for code in codes:
    for i in range(1,4):
        url = f"https://lush.co.kr/goods/goods_list.php?page={i}&cateCd={code}"
        driver.get(url)
        driver.implicitly_wait(60)
        time.sleep(1)

        try:
            r = driver.page_source
            soup = BeautifulSoup(r, 'html.parser')
            prd_list = soup.select(".prdList li")
            for i in range(len(prd_list)):
                try:
                :# 외부
                    prd_cd = prd_list[i].select_one(".thumbnail .choice .btn-open-win")["data-goods-no"]
                    product_name = prd_list[i].select_one(".prdinfo .txt .prdName").get_text()
                    hashtag = prd_list[i].select_one(". ")   
                    
                    # 내부
                    url2 = f"https://lush.co.kr/goods/goods_view.php?goodsNo={prd_cd}"
                    driver.get(url2)
                    driver.implicitly_wait(60)
                    time.sleep(1)
                    r2 = driver.page_source
                    soup2 = BeautifulSoup(r2, 'html.parser')
                    
                    video_url = soup2.select_one("#external-video iframe")["src"]
    
                    csv_writer.writerow((product_name, video_url))
                except:
                    continue
        except:
            continue
            

driver.quit()
