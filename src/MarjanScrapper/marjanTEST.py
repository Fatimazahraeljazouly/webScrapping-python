from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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
time.sleep(3)  # Attendre le chargement initial de la page

# Scrolling et scraping
scroll_pause_time = 3  # Temps d'attente après chaque défilement
max_scrolls = 20  # Limite pour éviter une boucle infinie
previous_count = 0  # Nombre d'éléments avant le scroll

for scroll in range(max_scrolls):
    print(f"Scrolling pass: {scroll + 1}")

    # Attendre que les nouveaux éléments se chargent
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ais-InfiniteHits-item div.product-item-info'))
        )
    except TimeoutException:
        print("Timeout waiting for new elements.")
        break

    # Extraire les produits visibles
    items = driver.find_elements(By.CSS_SELECTOR, 'li.ais-InfiniteHits-item div.product-item-info')
    print(f"Found {len(items)} items on this pass.")

    # Si aucun nouvel élément n'est ajouté, arrêter le défilement
    if len(items) == previous_count:
        print("No new items found. Stopping.")
        break

    previous_count = len(items)  # Mettre à jour le compteur

    for index, item in enumerate(items):
        try:
            # Déboguer les sélecteurs et extraire les données
            image = item.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
            url = item.find_element(By.CSS_SELECTOR, 'a.product-item-photo.product-item-photo-algolia.result').get_attribute("href")
            title = item.find_element(By.CSS_SELECTOR, "a.product-item-link").text
            try:
                old_price1 = item.find_element(By.CSS_SELECTOR, "span.old-price span.price").text
                old_price2 = item.find_element(By.CSS_SELECTOR, "span.float-number").text
                old_price = f"{old_price1},{old_price2}DH"
            except NoSuchElementException:
                old_price = "N/A"

            try:
                current_price1 = item.find_element(By.CSS_SELECTOR, "span.price").text
                current_price2 = item.find_element(By.CSS_SELECTOR, "span.float-number").text
                current_price = f"{current_price1},{current_price2}DH"
            except NoSuchElementException:
                current_price = "N/A"

            data_product = {
                "image": image,
                "url": url,
                "title": title,
                "old_price": old_price,
                "current_price": current_price,
            }
            print(f"Item {index + 1}: {data_product}")
            if data_product not in data:
                data.append(data_product)
        except NoSuchElementException as e:
            print(f"Element not found for item {index + 1}: {e}")

    # Scroller vers le bas pour charger plus de contenu
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)  # Attendre le chargement de la page

# Fermer le driver
driver.quit()

# Sauvegarder les données dans un fichier JSON
with open("marjane_data.json", "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"Scraping completed. {len(data)} items collected.")
