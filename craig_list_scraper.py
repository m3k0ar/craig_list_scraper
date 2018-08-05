
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time 

from bs4 import BeautifulSoup
import urllib.request

class CraigListScraper(object):
    def __init__(self, ort, max_preis):
        self.ort = ort
        # self.plz = plz
        self.max_preis = max_preis
        # self.radius = radius

        self.url = f"https://{ort}.craigslist.de/d/zum-verkauf/search/sss?max_price={max_preis}"

    # print out url    
    # def test(self):
    #     print(self.url)

        # Firefox als Webbrowser
        self.driver = webdriver.Firefox()
        self.delay = 10     # time to wait till the website loads up

    def load_website(self):
        self.driver.get(self.url)
        try:
            wait = WebDriverWait(self.driver, self.delay)
            wait.until(EC.presence_of_element_located((By.ID, "searchform")))
            print("Page fully loaded")
        except TimeoutException:
            print("Loading took too much time, Timeout within 10s")

    def extrahiereAnzeigeInfo(self):
        all_post = self.driver.find_elements_by_class_name("result-row")
        # print(all_post)
        datums = []
        titels = []
        preise = []
        for post in all_post:
            # print(post.text)
            titel = post.text.split('€')
            # print(titel)
        
            if titel[0] == '':
                titel = titel[1]
                # print(titel)
            else:
                titel = titel[0]
                # print(titel)
            
            titel = titel.split("\n")
            preis = titel[0]
            # print(preis)
            titel = titel[-1]
            # print(titel)

            titel = titel.split(" ")
            monat = titel[0]
            tag = titel[1]
            titel = ' '.join(titel[2:])
            datum = tag + ". " + monat

            # print("Preis: " + preis + "€")
            # print("Titel: " + titel)
            # print("Datum: " + datum)

            preise.append(preis)
            titels.append(titel)
            datums.append(datum)
        return preise, titels, datums


    def extrahiereAnzeigeURL(self):  
        url_list = []
        html_page = urllib.request.urlopen(self.url)
        soup = BeautifulSoup(html_page, "lxml")
        for link in soup.find_all("a", {"class": "result-title hdrlnk"}):
            print(link["href"])
            url_list.append(link["href"])
        return url_list

    def quit_browser(self):
        self.driver.close()


ort = 'berlin'
max_preis = '1000'

# Scraper Object
scraper = CraigListScraper(ort, max_preis)      

scraper.load_website()
# sleep(5)
scraper.extrahiereAnzeigeInfo()
# scraper.extrahiereAnzeigeURL()
# scraper.test()
preise, titels, datums = scraper.extrahiereAnzeigeInfo()
print(titels)
scraper.quit_browser()

