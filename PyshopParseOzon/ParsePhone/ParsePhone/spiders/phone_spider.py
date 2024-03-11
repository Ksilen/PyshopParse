import requests
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import time
import webbrowser
from selenium.webdriver.chrome.options import Options
import pyautogui
import pyperclip
import pandas as pd
import undetected_chromedriver as uc
from lxml import html

class WebsiteSpider(scrapy.Spider):
    name = "website"
    start_urls = "https://www.ozon.ru/category/smartfony-15502/?sorting=rating"
    # start_urls = ""
    @staticmethod
    def __webdriver_spider(url):
        webbrowser.open(url, new=2)
        time.sleep(3)
        pyautogui.press('F12')
        time.sleep(3)
        pyautogui.press('F2')
        time.sleep(2)
        pyautogui.press('left')
        pyautogui.hotkey('ctrl','a')
        time.sleep(1)
        pyautogui.hotkey('ctrl','c')
        x = pyperclip.paste()
        pyautogui.hotkey('ctrl','w')
        return x

    def start_requests(self):
        phone_total = 100
        page = 1
        url_main = self.start_urls
        count_phone = 0
        list_system = []

        while count_phone <= phone_total:
            phone_link = self.__webdriver_spider(url=url_main)
            url_main = f"https://www.ozon.ru/category/smartfony-15502/?page={page}" \
                      f"&sorting=rating"
            page += 1
            phones = html.fromstring(phone_link).xpath(
                '//div[@class="iv7"]/a[starts-with(@href,product)]/@href'
            )
            for link in phones:
                url_link = f"https://www.ozon.ru{str(link).split('?')[0]}"
                print(url_link)
                phone = self.__webdriver_spider(url=url_link)
                phone_system = html.fromstring(phone).xpath(
                    '//dl[@class ="j3u"]/dd[contains(text(),"iOS ") or contains(text(),"Android ")]/text()'
                )
                print("F: ",phone_system)
                if phone_system:
                    count_phone += 1
                    list_system.append(phone_system)
                    if count_phone >= phone_total:
                        break

            if count_phone >= phone_total:
                break

        df = pd.Series(system[0] for system in list_system)
        answer = df.value_counts(sort=True).to_dict()
        for key, value in answer.items():
            with open('system_versions.txt', 'a', encoding='utf-8') as f:
               f.write(f"{key} - {value}\n")