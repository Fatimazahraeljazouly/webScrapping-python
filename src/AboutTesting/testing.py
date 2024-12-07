from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--headless")

driver_path = "C:/Users/Eljazouly/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

website = "https://books.toscrape.com/"
products = []

driver.get(website)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "product_pod"))
)

items = driver.find_elements(By.CLASS_NAME, "product_pod")

for item in items:
    try:
        title = item.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
        price = item.find_element(By.CLASS_NAME, "price_color").text
        availability = item.find_element(By.CLASS_NAME, "availability").get_attribute("class").split()[0]
        image = item.find_element(By.CSS_SELECTOR, ".image_container img").get_attribute("src")
        url = item.find_element(By.CSS_SELECTOR, ".image_container a").get_attribute("href")
        star_rating = item.find_element(By.CLASS_NAME, "star-rating").get_attribute("class").split()[1]

        price = float(price.replace('£', '').strip())  # Assuming currency symbol is £

        products.append({
            "title": title,
            "price": price,
            "availability": availability,
            "image": image,
            "url": url,
            "star_rating": star_rating
        })
    except Exception as e:
        print(f"Error processing a product: {e}")

driver.quit()

for product in products:
    print("\n--- Product ---")
    for key, value in product.items():
        print(f"{key}: {value}")


maFile=open("data.json","r")
maFile.read()