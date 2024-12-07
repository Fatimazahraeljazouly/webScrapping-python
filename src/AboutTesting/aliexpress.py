from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
chrome_options = Options()
chrome_options.add_argument("--headless")
service=Service(executable_path=ChromeDriverManager().install())
driver=webdriver.Chrome(service=service)
website = "https://fr.aliexpress.com/w/wholesale-electromenage.html?spm=a2g0o.productlist.search.0"
driver.get(website)

myProducts=[]
driver.get(website)

items = driver.find_elements(By.CSS_SELECTOR,"div.multi--outWrapper--SeJ")
print(items)
for item in items :
    try:
        name="refrigirateur avec congilateur"
        #title=item.find_element()
        image=item.find_element(By.CSS_SELECTOR,'div.box-image a').get_attribute("href")
        url=item.find_element(By.CSS_SELECTOR,'div.box-image a').get_attribute("href")
        brand=item.find_element(By.CSS_SELECTOR,"span.brand").text
        ref=item.find_element(By.CSS_SELECTOR,"span.ref").text
        old_price=item.find_element(By.CSS_SELECTOR,"span.price").text
        current_price=item.find_element(By.CSS_SELECTOR,"span.price").text
        discount=item.find_element(By.CSS_SELECTOR,"span.price-discount-percent").text
        myProducts.append({
            "image": image,
            "url": url,
            "brand":brand,
            "ref":ref,
            "old_price":old_price,
            "current_price":current_price,
            "discount":discount
        })
    except Exception as e:
        print(f"Error processing a product: {e}")

driver.quit()

for product in myProducts:
    print("\n--- Product ---")
    for key, value in product.items():
        print(f"{key}: {value}")
