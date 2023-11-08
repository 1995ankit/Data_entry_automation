import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import os
from selenium.webdriver.common.keys import Keys

GOOGLE_FORM_URL = 'https://forms.gle/yiB3GCdWghpXphxSA'
zillow_filtered_url = 'https://www.zillow.com/san-francisco-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-122.63417331103516%2C%22east%22%3A-122.23248568896484%2C%22south%22%3A37.66829531378608%2C%22north%22%3A37.88213396734814%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A529867%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22San%20Francisco%20CA%22%7D'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
response = requests.get(zillow_filtered_url, headers=headers)
webpage = response.text
soup = BeautifulSoup(webpage, 'html.parser')
print(soup.title)

url = []
address = []
price_list = []

listings_url = soup.select(selector='.property-card-data a')
for listing in listings_url:
    if 'https' in listing['href']:
        url.append(listing['href'])
    else:
        url.append(f'https://www.zillow.com{listing["href"]}')
    address.append(listing.text)
prices = soup.select(selector='.property-card-data span')
for price in prices:
    if '+' in price.text:
        price_list.append(price.text.split('+')[0])
    else:
        price_list.append(price.text.split('/')[0])
prices = [price.split('$')[1] for price in price_list]
prices = [int(price.replace(',', '')) for price in prices]

# for i in range(len(url)):
#     print(address[i], " for ", prices[i], ' USD', ":", url[i])

CHROME_DRIVER_PATH = ChromeDriverManager().install()
driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH))
for n in range(len(prices)):
    driver.get(GOOGLE_FORM_URL)
    addr = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    addr.send_keys(address[n])
    sleep(1)
    price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(prices[n])
    sleep(1)
    link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(url[n])
    sleep(1)
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    sleep(2)


