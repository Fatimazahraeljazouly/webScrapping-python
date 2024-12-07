from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
data = []

driver.get(
    'https://www.amazon.fr/s?k=electromenager&i=kitchen&crid=48USSZ7GNY0G&sprefix=electro%2Ckitchen%2C121&ref=nb_sb_ss_ts-doa-p_2_7')

while True:

    items = driver.find_elements(By.CSS_SELECTOR,
                                 'div.puis-card-container.s-card-container.s-overflow-hidden.aok-relative.puis-include-content-margin.puis.puis-v4s73penu6ddq273xf3q9lbp2k.s-latency-cf-section.puis-card-border')

    for item in items:
        try:
            title = item.find_element(By.CSS_SELECTOR, 'span.a-size-medium.a-color-base.a-text-normal').text
            rating = item.find_element(By.CSS_SELECTOR, 'span.a-icon-alt').get_attribute('innerText')
            first_price = item.find_element(By.CSS_SELECTOR,
    'span.a-price.a-text-price span.a-offscreen').get_attribute('innerText')
            lastPrice = item.find_element(By.CSS_SELECTOR, 'span.a-price span.a-offscreen').get_attribute("innerText")
            productçdata = {
                "title": title,
                "rating": rating,
                "first_price": first_price,
                "last_price": lastPrice
            }

            data.append(productçdata)

            print(f'Title: {title},rating: {rating}, firstPrice: {first_price}, lastPrice: {lastPrice}')
        except NoSuchElementException:
            print("Element with '.product-item-info' not found in this item.")

    try:  # class="s-pagination-item s-pagination-selected"
        # class="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator"
        next_button = driver.find_element(By.CSS_SELECTOR,
                                          'a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-button-accessibility.s-pagination-separator')
        next_button.click()

        time.sleep(2)
    except (NoSuchElementException, TimeoutException):
        print("No more pages found or 'Next' button not available.")
        break

driver.quit()

with open("data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)