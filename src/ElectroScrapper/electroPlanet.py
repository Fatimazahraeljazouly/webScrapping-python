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
data =[]

# Variables de base pour le scraping
base_url = 'https://www.electroplanet.ma/recherche?q=electromenage&p='
page_number = 1  # Incrémentation de page
close = False

while True and not close :
    # Construction dynamique de l'URL avec la variable `p`
    url = f"{base_url}{page_number}"
    driver.get(url)
    time.sleep(2)  # Attendre le chargement de la page

    # Scraper les éléments de la page
    items = driver.find_elements(By.CSS_SELECTOR, 'div.item-inner')

    # Extraire les informations des produits
    for item in items:
        try:
            image = item.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
            url = item.find_element(By.CSS_SELECTOR, 'div.box-image a').get_attribute("href")
            brand = item.find_element(By.CSS_SELECTOR, "span.brand").text
            ref = item.find_element(By.CSS_SELECTOR, "span.ref").text
            old_price = item.find_element(By.CSS_SELECTOR, "span.price").text
            current_price = item.find_element(By.CSS_SELECTOR, "span.price").text
            #discount = item.find_element(By.CSS_SELECTOR, "div.price-box-special span.price-discount-percent").get_attribute("innerText")
            data_product = {
                "image": image,
                "url": url,
                "brand":brand,
                "ref":ref,
                "old_price":old_price,
                "current_price":current_price
                #"discount":discount
            }
            print(data_product)
            data.append(data_product)
        except NoSuchElementException:
            print("Element with '.product-item-info' not found in this item.")

    # Vérifier la présence d'un bouton "Next" (ou similaire) pour continuer, sinon arrêter
    try:
        # Tester si un bouton "Next" est présent et cliquer pour vérifier la présence de la page suivante
        next_button = driver.find_element(By.CSS_SELECTOR, 'li a.action.next')
        page_number += 1  # Incrémenter le numéro de page
        if page_number  == 6:
            close=True
        time.sleep(2)  # Pause pour éviter de surcharger le site
    except (NoSuchElementException, TimeoutException):
        print("No more pages found or 'Next' button not available.")
        break

# Fermer le driver à la fin
driver.quit()

with open("electroplanet.json", "w", encoding="utf-8") as json_file:
    json.dump(data,json_file,ensure_ascii=False,indent=4)