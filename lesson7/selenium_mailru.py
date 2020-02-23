from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.opera.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pymongo import MongoClient

from datetime import datetime as dt, timedelta as td
import locale
locale.setlocale(locale.LC_ALL, 'ru_RU')

import time

class Login:

    def __init__(self):
        self.login = 'study.ai_172@mail.ru'
        self.password = 'NewPassword172'

    def get_message(self):
        driver = webdriver.Opera()
        driver.get('https://mail.ru')

        login_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mailbox:login'))
        )
        time.sleep(1)
        login_box.send_keys((self.login, Keys.ENTER))

        password_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'mailbox:password'))
        )
        time.sleep(1)
        password_box.send_keys((self.password, Keys.ENTER))

        first_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="dataset__items"]/a'))
        )
        time.sleep(1)
        driver.get(first_message.get_attribute('href'))

        return driver

    def get_data(self):

        global driver

        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="thread__subject-line"]/h2'))
        ).text

        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="letter-body"]'))
        ).text

        contact = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="letter-contact"]'))
        ).get_attribute('title')

        date_ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="letter__date"]'))
        ).text

        def date_process(date_):
            try:
                if '2019' in date_:
                    d = str(date_.split(' 2019')[0])
                    d = str(dt.strptime(d, '%d %B'))[5:-9]
                    y = '2019'
                    t = str(date_.split(', ')[-1])

                    r = '-'.join([y, d]) + ' ' + t

                elif '2018' in date_:
                    d = str(date_.split(' 2018')[0])
                    d = str(dt.strptime(d, '%d %B'))[5:-9]
                    y = '2018'
                    t = str(date_.split(', ')[-1])

                    r = '-'.join([y, d]) + ' ' + t

                elif 'Сегодня' in date_:
                    d = str(dt.now().date()).split()[0]
                    t = str(date_.split(', ')[-1])

                    r = ' '.join([d, t])

                else:
                    d = '2020' + str(dt.strptime(date_.split(', ')[0], '%d %B'))[4:-9]
                    t = str(date_.split(', ')[-1])

                    r = ' '.join([d, t])

                return r
            except Exception as e:
                print(date_)
                print(e)


        next_ = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="button2 button2_has-ico button2_arrow-down button2_pure button2_short button2_compact button2_ico-text-top button2_hover-support js-shortcut"]'))
        )
        data = {
            'contact': contact,
            'title': title,
            'date': date_process(date_),
            'text': body.split('\n')[0] + '...',
        }
        next_.click()

        return data


class Mongo:

    def __init__(self, blank=False):
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.items = client['messages'].items
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

    login = Login()
    driver = login.get_message()
    mongo = Mongo(blank=True)
    while True:
        try:
            data = login.get_data()
            if not mongo.contains(data):
                mongo.insert(data)
            print(data)
        except Exception as e:
            # print(e)
            driver.quit()
            break

