from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from urllib.parse import quote
import time
import pandas as pd
import os  
import random

options = Options()
options.add_argument("window-size=1280,1000")
options.add_argument("--log-level=3")
options.add_argument("--disable-geolocation")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox") 
options.add_argument("--ignore-certificate-errors") 

#options.add_argument("--headless")  

driver_path = r"C:\Users\BojackHors3man\?????????????\edgedriver_win64\msedgedriver.exe"
service = EdgeService(driver_path)
driver = webdriver.Edge(service=service, options=options)


def marketlist2marketlinks(listexcelpath):
    df = pd.read_excel(listexcelpath)
    
    marketnwithl = []
    
    for index, row in df.iterrows():
        market_name = row['نام فروشگاه']
        market_link = row['لینک فروشگاه']
        marketnwithl.append((market_name, market_link))
    
    return marketnwithl

def calculate_discount(entry_price, old_price):
    try:
        current_price = float(entry_price.replace(",", "").strip())
        
        if not old_price:
            return None  
        
        old_price = float(old_price.replace(",", "").strip())
        
        if old_price > 0:
            discount_percent = ((old_price - current_price) / old_price) * 100
            return round(discount_percent, 2)
        else:
            return None
    except Exception as e:
        return None
    
def scroll_to_bottom(driver, max_idle_time=3, scroll_pause_time=0.2):
    """
    Scrolls to the bottom of the page with natural up/down movement, 
    and stops if no new content loads within 'max_idle_time' seconds.
    
    Args:
        driver: Selenium WebDriver instance.
        max_idle_time: Seconds to wait after no new content loads before stopping.
        scroll_pause_time: Seconds to wait between each scroll move.
    """
    last_height = driver.execute_script("return document.body.scrollHeight")
    idle_start_time = None

    while True:
        driver.execute_script("window.scrollBy(0, 5000);")
        time.sleep(scroll_pause_time)
        
        scroll_up_distance = random.randint(300, 800)
        driver.execute_script(f"window.scrollBy(0, -{scroll_up_distance});")
        time.sleep(0.1) 

        driver.execute_script("window.scrollBy(0, 5000);")
        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            if idle_start_time is None:
                idle_start_time = time.time()
            elif time.time() - idle_start_time >= max_idle_time:
                print("✅ No new content detected for {} seconds. Finished scrolling.".format(max_idle_time))
                break
        else:
            idle_start_time = None
            last_height = new_height

def select_location(driver, city_name, mahale_name):
    driver.get("https://express.snapp.market")

    wait = WebDriverWait(driver, 60)
    city_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='انتخاب شهر']")))
    city_button.click()
    driver.delete_all_cookies()

    search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='جستجوی نام شهر']")))
    search_input.send_keys(city_name)
    driver.delete_all_cookies()

    city_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//li[text()='{city_name}']")))
    city_option.click()
    driver.delete_all_cookies()

    mahale_search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@class='ant-select-selection-search-input']")))
    mahale_search_input.send_keys(mahale_name)

    options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='rc-virtual-list-holder-inner']//div[@class='ant-select-item ant-select-item-option']")))
    print(f"Found {len(options)} Location")

    if len(options) > 0:
        options[0].click()  

    confirm_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[span[text()='تأیید موقعیت روی نقشه']]")))
    confirm_button.click()

def loc_marketex(driver, scroll_to_bottom): 
    wait = WebDriverWait(driver, 10)
    driver.delete_all_cookies()

    view_all_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='view-all-vendors']//button")))
    view_all_button.click()
    driver.delete_all_cookies()

    try : 
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='vendor-card']"))
        )
    except:
        print("No Market in your Selectded Mahale ! ⛔")

    scroll_to_bottom(driver)

    cards = driver.find_elements(By.XPATH, "//div[@data-testid='vendor-card']")

    data = []
    marketlinks=[]

    for card in cards:
        tracker = card.get_attribute('data-tracker') or ''
        vendor_id = None
        if "clickVendorCard#" in tracker:
            try:
                vendor_id = tracker.split("click:clickVendorCard#")[-1]
            except:
                vendor_id = None

        try:
            name = card.find_element(By.XPATH, ".//span[contains(@class, 'ant-typography-ellipsis')]").text
        except:
            name = ""

        try:
            rating = card.find_element(By.XPATH, ".//div[contains(@class, 'sc-imwsjW')]").text
        except:
            rating = ""

        try:
            delivery_time = card.find_element(By.XPATH, ".//article").text
        except:
            delivery_time = ""

        try:
            delivery_price = card.find_element(By.XPATH, ".//div[contains(@class,'dTlnZm')]").text
        except:
            delivery_price = ""

        try:
            image = card.find_element(By.TAG_NAME, "img").get_attribute("src")
        except:
            image = ""

        try:
            if vendor_id and name:
                encoded_name = quote(name, safe='')
                link = f"https://express.snapp.market/supermarket/{encoded_name}/{vendor_id}"
                marketlinks.append(link)
            else:
                link = "" 
        except Exception as e:
            link = "" 


        data.append({
            "نام فروشگاه": name,
            "امتیاز": rating,
            "لینک فروشگاه": link,
            "لوگو": image
        })

    df = pd.DataFrame(data)
    df.to_excel("Supermarkets_list.xlsx", index=False)
    print("✅Supermarkets.xlsx")

    print(f"{len(marketlinks)} Markets✅ ")
    return marketlinks

def extract_supermarket_data(driver, scroll_to_bottom, marketlinks, file_name , csv_file_path):
    all_supermarket_data = {}
    for supermarket, link in marketlinks:
        print(f"{supermarket}")

        print(f"\n\nلینک: {link}")

        drink_category_link = link.rstrip('/') + "/vendor-category/731215?params=%5B%7B%22name%22%3A%22subCategory%22%2C%22value%22%3A%5B%22731306%22%5D%7D%5D"
        print(f"Drinks..")

        subCategory = 731306
        category_id = 731215

        driver.get(drink_category_link)

        supermarket_name = supermarket

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.clickable.isProductCollection'))
            )

            scroll_to_bottom(driver)

            products = driver.find_elements(By.CSS_SELECTOR, 'div.clickable.isProductCollection')

            print(f"CNT : {len(products)}")

            product_list = []
            for idx, product in enumerate(products, start=1):

                product_id = None
                name = None
                price = None
                img = None
                old_price = None
                discount_percent = None

                try:
                    data_tracker = product.get_attribute('data-tracker')
                    if data_tracker:
                        product_id = data_tracker.split('#')[-1] 
                except Exception as e:
                    product_id = None
            
                try:
                    name = product.find_element(By.CSS_SELECTOR, 'span.ant-typography').text.strip()
                except:
                    name = None

                try:
                    price = product.find_element(By.CSS_SELECTOR, 'span.price').text.strip()
                except:
                    price = None

                try:
                    product_div = product.find_element(By.CSS_SELECTOR, 'div.sc-iHmpnF.dgaJLH')
                    img_elements = product_div.find_elements(By.CSS_SELECTOR, 'img')                
                    for img_element in img_elements:
                        img_src = img_element.get_attribute('src')
                        if '/product-hub/' in img_src and not img_src.endswith('.svg') and 'Placeholder.svg' not in img_src:
                            img = img_src 
                            break       
                except Exception as e:
                    img = None

                try:
                    old_price = product.find_element(By.CSS_SELECTOR, 'span.del').text.strip()
                except:
                    old_price = None

                try:
                    discount_percent = calculate_discount(price, old_price)
                except:
                    discount_percent = None

                if not name or not price or not img:
                    print(f"BAD : ({idx}): name={name}, price={price}, img={img}")

                product_list.append({
                    "نام محصول": name,
                    "قیمت فعلی": price,
                    "قیمت قبل از تخفیف": old_price,
                    "درصد تخفیف": discount_percent,
                    "لینک تصویر": img,
                    "product_id": product_id,                    
                    "subCategory" : subCategory,
                    "category_id" : category_id
                })

            supermarket_data = {"نوشیدنی": product_list}
            all_supermarket_data[supermarket_name] = supermarket_data

        except Exception as e:
            print(f"ERROR IN THE D P LINK! {e}")
            continue



    with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
        for supermarket, categories in all_supermarket_data.items():
            for category, products in categories.items():
                df = pd.DataFrame(products)
                sheet_name = f"{supermarket}" #[:31]  # Excel limit = 31 characters
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                output_path = os.path.abspath(file_name)
    # CSV
    excel_file_path = output_path
    excel_data = pd.read_excel(excel_file_path, sheet_name=None)
    if os.path.exists(excel_file_path):
       os.remove(excel_file_path)
    csv_data = []
    for sheet_name, df in excel_data.items():
        for index, row in df.iterrows():
            csv_data.append({
                'Supermarket Name': sheet_name,
                'Product Name': row.get('نام محصول', ''),
                'Current Price': row.get('قیمت فعلی', ''),
                'Old Price': row.get('قیمت قبل از تخفیف', ''),
                'Discount Percent': row.get('درصد تخفیف', ''),
                'Product ID': row.get('product_id', ''),
                'Sub Category': row.get('subCategory', ''),
                'Category ID': row.get('category_id', ''),
                'Image Link': row.get('لینک تصویر', '')
            })
            csv_df = pd.DataFrame(csv_data)
        csv_df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')


#Setup :
city_name = "تهران"
mahale_name = "محله شهرک اکباتان تهران"
file_name = 'supermarket_data.xlsx'
csv_file_path = r'C:\Users\BojackHors3man\?????????????\supermarket_data.csv'


#0
# select_location(driver, city_name, mahale_name)
# loc_marketex(driver, scroll_to_bottom)

listexcelpath = r'C:\Users\BojackHors3man\?????????????\Supermarkets_list.xlsx'
marketlinks = marketlist2marketlinks(listexcelpath)


extract_supermarket_data(driver, scroll_to_bottom, marketlinks, file_name , csv_file_path)