import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
search_th = input("Searching for: ")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.amazon.com/")
search = driver.find_element(By.NAME, "field-keywords")
search.send_keys(search_th)
search.send_keys(Keys.RETURN)

product_name = []
product_price = []

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//*[@class="s-pagination-item s-pagination-disabled"]')))
except:
    driver.quit()
links = driver.find_element(By.XPATH, '//*[@class="s-pagination-item s-pagination-disabled"]')
for i in range(int(links.text) - 10):
    page_ = i + 1
    # scraping
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))
    for item in items:
        # find name
        name = item.find_element(By.XPATH, './/span[contains(@class, "a-text-normal")]')
        product_name.append(name.text)

        whole_price = item.find_elements_by_xpath('.//span[@class="a-price-whole"]')
        fraction_price = item.find_elements_by_xpath('.//span[@class="a-price-fraction"]')
        if whole_price != [] and fraction_price != []:
            price = '.'.join([whole_price[0].text, fraction_price[0].text])
        else:
            price = 0
        product_price.append(price)

    driver.implicitly_wait(3)
    driver.find_element(By.XPATH, '//a[contains(@class, "s-pagination-next")]').click()
    print(f"Page {page_} grabbed")

df = pd.DataFrame({
    'product_name': product_name,
    'product_price': product_price
})

df.to_csv('data_results.csv', index=False)
