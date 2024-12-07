from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import json

# Configure Chrome options
from selenium.webdriver.chrome.options import Options

from src.testing import price

options = Options()
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
)
options.add_argument("--headless")  # Run in headless mode (optional)
options.add_argument("--disable-blink-features=AutomationControlled")
# Uncomment below to add proxy (optional)
# options.add_argument('--proxy-server=http://your.proxy.server:port')

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

data = []

# Load the initial page
url = 'https://www.amazon.fr/s?k=electrom%C3%A9nager&i=kitchen&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1QYT6P10COGUE&sprefix=electrom%C3%A9nager%2Ckitchen%2C314&ref=nb_sb_noss_1'
driver.get(url)
time.sleep(random.uniform(3, 6))  # Random initial delay

while True:
    try:


        # Find all product items on the page
        items = driver.find_elements(By.CSS_SELECTOR, 'div.a-section.a-spacing-base')

        for item in items:
            try:
                href = item.find_element(By.CSS_SELECTOR, "a.a-link-normal.s-no-outline").get_attribute("href")
                title = item.find_element(By.CSS_SELECTOR, 'span.a-size-base-plus.a-color-base.a-text-normal').text
                #rating = item.find_element(By.CSS_SELECTOR, 'span.a-icon-alt').get_attribute('innerText')
                first_price = item.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
                last_price = item.find_element(By.CSS_SELECTOR, 'span.a-price-fraction').text
                currency=item.find_element(By.CSS_SELECTOR,"span.a-price-symbol").text
                full_price = f"{first_price},{last_price}{currency}"
                product_data = {
                    "title": title,
                    #"rating": rating,
                    "full_price": full_price,
                    "href": href,
                }

                # Avoid duplicate entries
                if not any(d["href"] == href for d in data):
                    data.append(product_data)
                print(product_data)
            except NoSuchElementException as e:
                print(f"Error scraping item: {e}")

        # Find and click the "Next" button
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 's-pagination-next')]"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            print("Moved to the next page.")
            time.sleep(random.uniform(3, 7))  # Allow page to load

            # Random delay between pages  next_button = WebDriverWait(driver, 10).until(
            #                 EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 's-pagination-item')]"))
            #             )
            #             next_button.click()
            #             time.sleep(random.uniform(3, 7))
        except TimeoutException:
            print("No more pages to scrape or 'Next' button not found.")
            break

    except Exception as e:
        print(f"Unexpected error: {e}")
        break

# Quit the driver
driver.quit()

# Save data to a JSON file
with open("amazon_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Scraping complete. {len(data)} products saved to 'amazon_data.json'.")
print("fuck u all ")
