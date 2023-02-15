import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

form_link = "https://forms.gle/Ss3SAAAqRr9bRGxy9"

zillow_url = "https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22mapBounds%22%3A%7B%22west%22%3A-122.67022170019531%2C%22east%22%3A-122.19643629980469%2C%22south%22%3A37.61365071716785%2C%22north%22%3A37.936579554637035%7D%2C%22mapZoom%22%3A11%2C%22isMapVisible%22%3Afalse%2C%22filterState%22%3A%7B%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%7D"
zillow_headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0",
    "Accept-Language": "en-US"
}

response = requests.get(url=zillow_url, headers=zillow_headers)
zillow_page = response.text
# print(zillow_page)

soup = BeautifulSoup(zillow_page, "html.parser")

all_link_tags = soup.select(".list-card-info a")
all_links = []
for x in all_link_tags:
    link = x["href"]
    # print(link)
    if "https" not in link:
        link = f"https://www.zillow.com{link}"
    all_links.append(link)
print(all_links)

all_address_tags = soup.select(".list-card-link address")
all_addresses = [x.get_text().split(" | ")[-1] for x in all_address_tags]
print(all_addresses)

all_price_tags = soup.select(".list-card-price")
all_prices = []
for x in all_price_tags:
    price = x.get_text().split("+")[0]
    if "/mo" not in price:
        price = f"{price}/mo"
    all_prices.append(price)
print(all_prices)


chrome_driver = Service("/Applications/chromedriver")
driver = webdriver.Chrome(service=chrome_driver)


for x in range(len(all_links)):
    driver.get(form_link)

    time.sleep(3)
    address_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    time.sleep(1)
    address_input.send_keys(all_addresses[x])
    time.sleep(1)
    price_input.send_keys(all_prices[x])
    time.sleep(1)
    link_input.send_keys(all_links[x])
    time.sleep(1)
    submit_button.click()



driver.quit()