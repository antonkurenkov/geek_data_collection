from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pymongo import MongoClient

def get_pages(driver):

    driver.get('https://www.mvideo.ru')
    while True:
        try:
            next_btn = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="gallery-layout sel-hits-block "]/div/div/div/div/a[@class="next-btn sel-hits-button-next"]')
                )
            )

            next_btn.click()
        except Exception as e:
            break

    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, '//div[@class="gallery-layout sel-hits-block "]/div/div/div/div/div/ul/li//a')
        )
    )

    urls = ['/'.join(item.get_attribute('href').split('/')[:5]) for item in items]
    u_unique = []
    for u in urls:
        if len(u_unique) < 20:
            if u not in u_unique:
                u_unique.append(u)

    return u_unique

def get_data(link):

    # global driver
    # driver: webdriver.Opera
    driver.get(link)

    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//h1[@class="e-h1 sel-product-title"]')
        )
    ).text

    price = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@class="c-pdp-price__current sel-product-tile-price"]')
        )
    ).text

    try:
        description = driver.find_element_by_xpath('//div[@class="collapse-text-initial"]').text
    except Exception as e:
        description = None

    data = {
        'title': title,
        'price': int(price.replace('¤', '').replace(' ', '')) if price else None,
        'description': description,
    }
    return data


class Mongo:

    def __init__(self, blank=False):
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.items = client['mvideo'].items
        if blank:
            self.items.delete_many({})

    def insert(self, entity):
        self.items.insert_one(entity)

    def head(self, num):
        objects = self.items.find().limit(num)
        for item in objects:
            print(item)

    def contains(self, item):
        return self.items.find(item).count()


if __name__ == '__main__':
    opera_options = Options()
    opera_options.add_argument('--start-maximized')
    driver = webdriver.Opera(options=opera_options)
    mongo = Mongo(blank=True)
    try:
        links = get_pages(driver)

        for link in links:
            data = get_data(link)
            if not mongo.contains(data):
                mongo.insert(data)
        driver.quit()
    except Exception as e:
        print(e)
        driver.quit()
