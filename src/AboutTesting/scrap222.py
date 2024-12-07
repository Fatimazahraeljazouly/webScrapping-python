from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_electroplanet_products(max_pages=10):
    # Configuration du driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Mode sans interface graphique
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # URL de départ
    website = "https://www.electroplanet.ma/recherche?q=electromenage"
    driver.get(website)

    myProducts = []
    page_number = 1
    max_products_per_page = 0  # Initialisé à 0, sera mis à jour après le premier chargement

    try:
        while page_number <= max_pages:
            print(f"Scraping page {page_number}")

            # Attendre que les produits soient chargés sur la page actuelle
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.product-item-info"))
            )

            # Récupérer les produits de la page actuelle
            items = driver.find_elements(By.CSS_SELECTOR, "div.product-item-info")
            if max_products_per_page == 0:
                max_products_per_page = len(items)  # Mettre à jour le nombre maximum de produits par page

            if len(items) != max_products_per_page:
                print(
                    f"Nombre de produits différent de la page précédente ({len(items)} au lieu de {max_products_per_page})")

            for item in items:
                try:
                    image = item.find_element(By.CSS_SELECTOR, "div.box-image a").get_attribute("href")
                    url = item.find_element(By.CSS_SELECTOR, "div.box-image a").get_attribute("href")
                    brand = item.find_element(By.CSS_SELECTOR, "span.brand").text
                    ref = item.find_element(By.CSS_SELECTOR, "span.ref").text
                    old_price = item.find_element(By.CSS_SELECTOR, "span.price").text
                    current_price = item.find_element(By.CSS_SELECTOR, "span.price").text
                    discount = item.find_element(By.CSS_SELECTOR, "span.price-discount-percent").text

                    myProducts.append({
                        "image": image,
                        "url": url,
                        "brand": brand,
                        "ref": ref,
                        "old_price": old_price,
                        "current_price": current_price,
                        "discount": discount
                    })
                except Exception as e:
                    print(f"Erreur lors du traitement d'un produit : {e}")

            # Rechercher le bouton "Suivant"
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next.action"))
                )

                # Cliquer sur le bouton "Suivant"
                next_button.click()

                # Attendre le chargement de la nouvelle page
                time.sleep(3)  # Délai pour le chargement de la page
                page_number += 1
            except Exception as e:
                print("Pas de bouton 'Suivant'. Fin de la pagination.")
                break
    except Exception as e:
        print(f"Erreur générale : {e}")
    finally:
        # Quitter le driver
        driver.quit()

    return myProducts


# Exécuter le scraping (avec un maximum de 10 pages)
products = scrape_electroplanet_products(max_pages=10)

# Afficher les résultats
for product in products:
    print("\n--- Product ---")
    for key, value in product.items():
        print(f"{key}: {value}")

print(f"\nTotal de produits scraped : {len(products)}")