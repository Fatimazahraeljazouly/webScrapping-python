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

base_url = 'https://www.jumia.ma/catalog/?q=electromenge'
page_number = 1
max_pages = 3
while page_number <= max_pages:
    url = f"{base_url}&page={page_number}#catalog-listing"
    print(f"Scraping page {page_number}: {url}")
    driver.get(url)
    time.sleep(2)

    items = driver.find_elements(By.CSS_SELECTOR, 'article.prd._fb.col.c-prd')

    for item in items:
        try:
            image = item.find_element(By.CSS_SELECTOR, 'img.img').get_attribute("data-src")
            url = item.find_element(By.CSS_SELECTOR, 'a.core').get_attribute("href")
            title = item.find_element(By.CSS_SELECTOR, "h3.name").text
            current_price = item.find_element(By.CSS_SELECTOR, "div.prc").text
            old_price = item.find_element(By.CSS_SELECTOR, "div.old").text if item.find_elements(By.CSS_SELECTOR, "div.old") else None

            data_product = {
                "image": image,
                "url": url,
                "name": title,
                "current_price": current_price,
                "old_price": old_price,
                "Website":"Jumia"
            }
            print(data_product)
            data.append(data_product)
        except NoSuchElementException as e:
            print("An element was not found in this item:", e)
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'a.pg[aria-label="Page suivante"]')
        page_number += 1  # Incrémenter le numéro de page
        time.sleep(2)  # Pause pour éviter de surcharger le site
    except NoSuchElementException:
        print("No more pages found. Stopping.")
        break

# Fermer le driver à la fin
driver.quit()

# Sauvegarder les données dans un fichier JSON
with open("jumia.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
