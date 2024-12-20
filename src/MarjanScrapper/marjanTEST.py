from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json

def scrape_marjane():
    """
    Scrapes data from Marjane's website and returns a list of dictionaries.
    """
    # Initialize WebDriver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    data = []

    # Base URL for scraping
    base_url = 'https://www.marjanemall.ma/catalogsearch/result/?q=electromenage&sortBy=magento2_prod_fr_products'

    # Load the first page
    driver.get(base_url)
    time.sleep(3)  # Wait for the initial page load

    # Scrolling and scraping configuration
    scroll_pause_time = 3  # Pause time after each scroll
    max_scrolls = 20  # Limit for scrolling attempts
    previous_count = 0  # Count of items before scrolling

    for scroll in range(max_scrolls):
        print(f"Scrolling pass: {scroll + 1}")

        # Wait for new elements to load
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li.ais-InfiniteHits-item div.product-item-info'))
            )
        except TimeoutException:
            print("Timeout waiting for new elements.")
            break

        # Extract visible products
        items = driver.find_elements(By.CSS_SELECTOR, 'li.ais-InfiniteHits-item div.product-item-info')
        print(f"Found {len(items)} items on this pass.")

        # Stop scrolling if no new items are found
        if len(items) == previous_count:
            print("No new items found. Stopping.")
            break

        previous_count = len(items)  # Update the item count

        for index, item in enumerate(items):
            try:
                # Extract product details
                image = item.find_element(By.CSS_SELECTOR, 'img.product-image-photo').get_attribute("src")
                url = item.find_element(By.CSS_SELECTOR, 'a.product-item-photo.product-item-photo-algolia.result').get_attribute("href")
                title = item.find_element(By.CSS_SELECTOR, "a.product-item-link").text

                try:
                    old_price = item.find_element(By.CSS_SELECTOR, "span.old-price span.price").text
                except NoSuchElementException:
                    old_price = "N/A"

                try:
                    current_price = item.find_element(By.CSS_SELECTOR, "span.price").text
                except NoSuchElementException:
                    current_price = "N/A"

                data_product = {
                    "image": image,
                    "url": url,
                    "title": title,
                    "old_price": old_price,
                    "current_price": current_price,
                    "Website": "Marjane"
                }
                print(f"Item {index + 1}: {data_product}")
                if data_product not in data:
                    data.append(data_product)
            except NoSuchElementException as e:
                print(f"Element not found for item {index + 1}: {e}")

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)  # Wait for the page to load

    # Close the WebDriver
    driver.quit()

    return data
