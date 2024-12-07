from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json

# Initialisation du WebDriver
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
data = []

# URL de base
base_url = 'https://www.marjanemall.ma/catalogsearch/result/?q=electromenage&sortBy=magento2_prod_fr_products'

# Charger la première page
driver.get(base_url)
time.sleep(5)  # Attendre le chargement initial de la page

# Scraping avec scrolling
scroll_pause_time = 5  # Temps d'attente après chaque défilement
previous_height = driver.execute_script("return document.body.scrollHeight")
max_scrolls = 10  # Limite pour éviter une boucle infinie

for _ in range(max_scrolls):
    # Extraire les produits visibles
    items = driver.find_elements(By.CSS_SELECTOR, 'li.ais-InfiniteHits-item div.product-item-info')

    for item in items:
        try:
            image = item.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
            url = item.find_element(By.CSS_SELECTOR,'a.product-item-photo.product-item-photo-algolia.result').get_attribute("href")
            title = item.find_element(By.CSS_SELECTOR, "a.product-item-link").text
            #ref = item.find_element(By.CSS_SELECTOR, "span.ref").text
            #old_price1 = item.find_element(By.CSS_SELECTOR, "span.old-price span.price").text
            #old_price2 = item.find_element(By.CSS_SELECTOR, "span.float-number").text
            #old_price = f"{old_price1},{old_price2}DH"
            current_price1 = item.find_element(By.CSS_SELECTOR, "span.price").text
            current_price2 = item.find_element(By.CSS_SELECTOR, "span.float-number").text
            current_price = f"{current_price1},{current_price2}DH"
            data_product = {
                "image": image,
                "url": url,
                "title": title,
                #"ref": ref,
                #"old_price": old_price,
                "current_price": current_price,
            }
            print(data_product)
            if data_product not in data:
                data.append(data_product)
        except NoSuchElementException:
            print("Element not found in this item.")

    # Scroller vers le bas pour charger plus de contenu
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)  # Attendre que la page se mette à jour

    # Vérifier si la hauteur de la page a changé
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == previous_height:
        print("Reached the end of the page.")
        break
    previous_height = new_height

# Fermer le driver
driver.quit()

# Sauvegarder les données dans un fichier JSON
with open("marjane_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
