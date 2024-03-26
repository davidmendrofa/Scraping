import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
# import requests
import pandas as pd
from openpyxl.workbook import Workbook



url = 'https://www.lamudi.co.id/yogyakarta/yogyakarta-1/house/buy/?page='
service = Service(executable_path = 'chromedriver.exe')
driver = webdriver.Chrome(service = service)

# html_text = requests.get(url).text
# print(html_text)

data = []
count_pages = 0
for page in range(1,51):
    driver.get(url+str(page))
    count_pages +=1
    print('scraping on page:', count_pages)
    try:
        WebDriverWait(driver,10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div.row.fullWidth.ClpBody'))
        )
        time.sleep(5)


        soup = BeautifulSoup(driver.page_source,'lxml')

        for item in soup.findAll('div',class_='ListingCell-AllInfo ListingUnit'):
            price = item.find('span',class_='PriceSection-FirstPrice').text.replace(' ','').replace('\n','').replace('Rp','')
            try: 
                bedroom_span = item.findAll('span', class_='KeyInformation-value_v2 KeyInformation-amenities-icon_v2')[0]
                if bedroom_span:
                    bedroom_icon = bedroom_span.find('span', class_='icon-bedrooms')
                    if bedroom_icon:
                        bedroom = bedroom_span.text.strip()
                        bedroom = int(bedroom)
            except: 
                bedroom = ''

            try:
                livingsize_span = item.findAll('span', class_='KeyInformation-value_v2 KeyInformation-amenities-icon_v2')[1]
                if livingsize_span:
                    livingsize_icon = livingsize_span.find('span', class_='icon-livingsize')
                    if livingsize_icon:
                        livingsize = livingsize_span.text.replace('m²','').strip()
                        livingsize = int(livingsize)
            except: 
                livingsize = ''

            try:
                landsize_span = item.findAll('span', class_='KeyInformation-value_v2 KeyInformation-amenities-icon_v2')[2]
                if landsize_span:
                    landsize_icon = landsize_span.find('span',class_='icon-land_size')
                    if landsize_icon:
                        landsize = landsize_span.text.replace('m²','').strip()
                        landsize = int(landsize)
            except: 
                landsize = ''
                
            
            data.append((price,bedroom,livingsize,landsize))
    
    except TimeoutException:
        print("Timeout: Unable to find the expected elements within the specified time.")

df = pd.DataFrame(data, columns=['harga_rp','kamar_tidur','luas_bangunan_m²','luas_tanah_m²'])
df.to_excel('Harga Rumah Yogyakarta di Lamudi.xlsx', index=False)
print('data telah tersimpan')

driver.close()


