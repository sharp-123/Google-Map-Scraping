import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import html2text
import requests
import json
import time
from py_trans import PyTranslator
import re
from base.items import BaseItem

class ScraperSpider(scrapy.Spider):
    name = 'scraper'
    
    SCROLL_PAUSE_TIME = 5
    
    
    def start_requests(self, **kwargs):
        with open('Input.txt', 'r', encoding='utf-8') as f:
            for city in f.readlines():
                city_name = city.split("\n")[0]
                query = f'{self.tag} in {city_name}'.replace(' ','+')
                yield SeleniumRequest(
                    url = f'https://www.google.co.in/maps/search/{query}',
                    callback = self.parse
                )

    
    def convert(self, text):
        # If you dont want to convert from any language to english comment this three lines and uncomment fourth line.
        py_t = PyTranslator(provider="google")
        text = py_t.translate(text, "en")
        return text['translation']
        #return text

    def parse(self, response):
        driver = response.meta['driver']
        # Get the current scroll position
        # arguments[0]
        element = driver.find_element(By.XPATH, "(//div[@class='m6QErb DxyBCb kA9KIf dS8AEf ecceSd'])[2]")
        print(f'[+] Accessing URL -> {response.url}')
        last_height = driver.execute_script("return arguments[0].scrollHeight", element)
        print(f'[+] Scrolling Start -> last height -> {last_height}\nScrolling Continuing .', end='')
        while True:
            # Scroll down to bottom
            driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', element)

            # Wait to load page
            time.sleep(self.SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return arguments[0].scrollHeight", element)
            print(f'.',end='')
            if new_height == last_height:
                print(f'\n[+] Scrolling Finished -> You have reached end of thr page -> Last Height -> {new_height}')
                break
            last_height = new_height

        res = scrapy.Selector(text = driver.page_source)
        urls = res.xpath('//div[@role="article"]/a/@href').getall()
        print(f'Got {len(urls)} items for url {response.url}')
        # 
        for url in urls:
            yield SeleniumRequest(
                url = url,
                callback = self.get_data,
                wait_time=10
            )

    def get_data(self, response):
        item = BaseItem()
        try:
            title = self.convert(response.xpath("//div[@class='tAiQdd']/div/div/h1/span/text()").get().replace(',','').replace('\n',''))
        except Exception as e:
            # print(f'Title{e}')
            title = 'NA'
            
        try:
            reviews = self.convert(response.xpath("//div[@class='tAiQdd']/div/div[2]/div/div/div[2]/span[2]/span/span/text()").get().replace(',','').replace('\n',''))
        except Exception as e:
            # print(f'Reviews{e}')
            
            reviews = 'NA'
            
        try:
            # address = self.convert(response.xpath('//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[7]/div[3]/button/div[1]/div[2]/div[1]/text()').get().replace(',','').replace('\n',''))
            w = response.xpath("//div[@class='Io6YTe fontBodyMedium']/text()").getall()
            address = w[0].replace(',','')
        except Exception as e:
            # print(f'address{e}')
            
            address = 'NA'
            
        try:
            w = response.xpath("//div[@class='Io6YTe fontBodyMedium']/text()").getall()
            for webs in w:
                # print(f'webs-{webs}')
                web = self.get_website_domain(webs)
                if web=="":
                    continue
                else:
                    print(f'web-{web}')
                    web_link = webs
                    # print(f'web_link-{web_link}')
                    break
            
        except Exception as e:
            # print(f'Web{e}')
            web_link = 'NA'
            
        try:
            opening_table = response.xpath("(//table)[1]/tbody/tr")
            res = {}
            for times in opening_table:
                day = self.convert(times.xpath(".//td[1]/div/text()").get().replace(',','').replace('\n',''))
                time = self.convert(times.xpath(".//td[2]/ul/li/text()").get().replace(',','').replace('\n',''))
                res[f'{day}'] = time
            print(res)
        except Exception as e:
            # print(f'Res{e}')
            
            res['Monday'] = 'NA'
            res['Tuesday'] = 'NA'
            res['Wednesday'] = 'NA'
            res['Thursday'] = 'NA'
            res['Friday'] = 'NA'
            res['Saturday'] = 'NA'
            res['Sunday'] = 'NA'
        
        try:
            w = response.xpath("//div[@class='Io6YTe fontBodyMedium']/text()").getall()
            for web in w:
                webs = self.get_number_from_html(web)
                if webs=="":
                    continue
                else:
                    phone = web
                    break
        except Exception as e:
            # print(f'phone{e}')
            
            phone='NA'
            
        try:
           w = response.xpath("//div[@class='Io6YTe fontBodyMedium']/text()").getall()
           for web in w:
               webs = self.is_valid_string(web)
               if not webs:
                   continue
               else:
                   plus_code = web
                   break
        except Exception as e:
            # print(f'web{e}')
            
            plus_code = 'NA'
        
        try:
            item['Title'] = title
            item['Reviews'] = reviews
            item['Address'] = address
            item['Monday'] = res['Monday']
            item['Tuesday'] = res['Tuesday']
            item['Wednesday'] = res['Wednesday']
            item['Thursday'] = res['Thursday']
            item['Friday'] = res['Friday']
            item['Saturday']= res['Saturday']
            item['Sunday'] = res['Sunday']
            item['Website'] = web_link
            item['Phone'] = phone
            item['PlusCode'] = plus_code
        except:
            item['Title'] = title
            item['Reviews'] = reviews
            item['Address'] = address
            item['Monday'] = res['Monday']
            item['Tuesday'] = res['Tuesday']
            item['Wednesday'] = res['environment']
            item['Thursday'] = res['Thursday']
            item['Friday'] = res['Friday']
            item['Saturday']= res['Saturday']
            item['Sunday'] = res['Sunday']
            item['Website'] = web_link
            item['Phone'] = phone
            item['PlusCode'] = plus_code
        
        # print(item)
        yield item
        
    def get_number_from_html(self,html):
    # Compile the regular expression
        pattern = re.compile(r'^[+0][\d\s-]+$')

        # Use the `findall` method to find all matches in the HTML
        matches = pattern.findall(html)

        # Return the first match, or an empty string if no match is found
        return matches[0] if matches else ""
    
    
    def get_website_domain(self, web):
        pattern = re.compile(r'[a-zA-Z]+\.[a-zA-Z]+')

        # Use the `findall` method to find a match
        matches = pattern.findall(web)

        # If a match is found, return the matching string
        return matches[0] if matches else ""
    

    def is_valid_string(self, string):
        # Compile the regular expression
        pattern = re.compile(r'[a-zA-Z0-9]+\+[a-zA-Z0-9]+')

        # Use the `search` method to find a match
        match = pattern.search(string)

        # If a match is found, return True
        if match:
            return True

        # If no match is found, return False
        return False