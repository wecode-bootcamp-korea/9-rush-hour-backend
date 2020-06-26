from selenium import webdriver
import csv

csv_filename = "lush_crawling outer2.csv"
csv_open     = open(csv_filename, "w+", encoding='utf-8')
csv_writer   = csv.writer(csv_open)
csv_writer.writerow( ('Name', 'Hashtag', 'Price','Product_ID', 'Sold Out', 'Vegan', 'New'))

#driver
driver = webdriver.Chrome('/Users/ethanjeong/chromedriver')
driver.implicitly_wait(4)

for i in range(1,3):
    driver.get(f"https://www.lush.co.kr/goods/goods_list.php?page={i}&cateCd=001001002")
    e = driver.find_elements_by_css_selector('.prdList li')
    for i in e:
        name     = i.find_element_by_css_selector('div.prdinfo .txt .prdName').text
        hashtag_str = ''

        hashtag  = i.find_element_by_css_selector('div.prdinfo .txt .shotdesc').text.split(' ')
        
        price    = i.find_element_by_css_selector('span.cost strong').text.replace(',', '')[2::]
        vegan    = i.find_elements_by_css_selector('.prdinfo .hot img')
        img_src  = vegan[0].get_attribute('src')
        sold_out = i.find_elements_by_css_selector('.prdinfo .conditions .soldout-img')

        #New, Vegan if statement
        if len(vegan) == 2 :
            vegan_list =True
            new_list = True
        elif len(vegan) == 1 and img_src[-3:] == 'jpg':
            vegan_list = False
            new_list = True
        elif len(vegan) == 1 and img_src[-3:] == 'png' :
            vegan_list = True
            new_list = False

        #sold_out if문
        if not sold_out :
            sold_out = False 
        else :
            sold_out = True
        
        product_id = i.find_element_by_css_selector('div > div > div.thumbnail > span > a.btn-open-win.-moslow').get_attribute('data-goods-no')
        csv_writer.writerow((name, hashtag, price, product_id, sold_out, vegan_list, new_list))
driver.close()
csv_open.close()
