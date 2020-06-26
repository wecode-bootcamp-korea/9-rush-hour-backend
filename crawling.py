from selenium import webdriver
import csv

# csv file
csv_filename = "bubble_bar1.csv"
csv_open = open(csv_filename, "w+", encoding="utf-8")
csv_writer = csv.writer(csv_open)
csv_writer.writerow( ('Image URL','Weight','Video URL','HTML Source','Pairing_ID'))
#csv_writer.writerow( ('Image URL','Weight','Video URL','Pairing_ID'))

# selenium
driver = webdriver.Chrome('/Users/ethanjeong/chromedriver')
driver.implicitly_wait(3)

# empty list 
name_list = []
image_list = []
weight_list = []
video_list = []
pairing_string = '' 
pairing_list = []
html_list = []

# for loop to get the length of a list 

driver.get("https://www.lush.co.kr/goods/goods_list.php?cateCd=001001002")
e = driver.find_elements_by_css_selector('.prdList li')
for i in e:
    name = i.find_element_by_css_selector('div.prdinfo .txt .prdName').text
    name_list.append(name)

#    for j in range(1,4):
#        driver.get(f"https://www.lush.co.kr/goods/goods_list.php?page={j}&cateCd=001001001")

for i in range(len(name_list)):
    page_link = driver.find_elements_by_xpath('//*[@id="wrap"]/div/div/div/div/div/div/ul/li/div/div/div/a')
    page_link[i].click()

            # Image
    img_elem = driver.find_element_by_xpath('//*[@id="mainImage"]/img').get_attribute('src')
    image_list.append(img_elem)

            # Weight
    weight = driver.find_element_by_xpath('//*[@id="frmView"]/div/div/div[3]/ul/li[2]/div/span').text[:-1]
    weight_list.append(weight)

            #Video URL
    try:
        video_url = driver.find_element_by_xpath('//*[@id="external-video"]/iframe').get_attribute('src')
        video_list.append(video_url)
    except:
        video_list.append('')
       
        # Pairing_ID
    pairing_item = driver.find_elements_by_xpath('//*[@id="detail"]/div/div/div/div/ul/li/div/div/div/a')   
    for x in pairing_item:
        x = x.get_attribute('href')[-3:]
            #pairing_string += x + ',' 
            #pairing_list.append(pairing_string)
        pairing_list.append(x)

       #HTML
    html_src = driver.find_element_by_css_selector('.txt-manual')
    html_list.append(html_src.get_attribute('innerHTML'))
            
    driver.back()
    csv_writer.writerow( (image_list[i], weight_list[i], video_list[i], html_list[i], pairing_list[i] ) )
        #csv_writer.writerow( (image_list[i], weight_list[i], video_list[i], pairing_list[i] ) )


driver.close()
csv_open.close()
