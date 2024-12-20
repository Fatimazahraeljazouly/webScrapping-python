from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import json


def scrape_electroplanet():
    """
    Scrapes data from ElectroPlanet's website and returns a list of dictionaries.
    """
    # Initialize WebDriver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    data = []

    # Base variables for scraping
    base_url = 'https://www.electroplanet.ma/recherche?q=electromenage&p='
    page_number = 1  # Start with the first page
    close = False

    while not close:
        # Dynamically construct the URL with the page number
        url = f"{base_url}{page_number}"
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Scrape elements on the page
        items = driver.find_elements(By.CSS_SELECTOR, 'div.item-inner')

        # Extract product information
        for item in items:
            try:
                image = item.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
                url = item.find_element(By.CSS_SELECTOR, 'div.box-image a').get_attribute("href")
                brand = item.find_element(By.CSS_SELECTOR, "span.brand").text
                ref = item.find_element(By.CSS_SELECTOR, "span.ref").text
                title = f"{ref} {brand}"
                old_priced = item.find_element(By.CSS_SELECTOR, "span.price").text
                old_price = f"{old_priced}Dh"
                current_priced = item.find_element(By.CSS_SELECTOR, "span.price").text
                current_price = f"{current_priced}Dh"
                data_product = {
                    "image": image,
                    "url": url,
                    "title": title,
                    "old_price": old_price,
                    "current_price": current_price,
                    "Website": "ElectroPlanet"
                }
                print(data_product)
                data.append(data_product)
            except NoSuchElementException:
                print("Element with '.product-item-info' not found in this item.")

        # Check for "Next" button to continue or stop
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, 'li a.action.next')
            page_number += 1
            if page_number == 6:  # Limit to 5 pages
                close = True
            time.sleep(2)  # Pause to avoid overloading the site
        except (NoSuchElementException, TimeoutException):
            print("No more pages found or 'Next' button not available.")
            break

    # Close the driver at the end
    driver.quit()

    return data
