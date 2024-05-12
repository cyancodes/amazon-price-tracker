import requests
from bs4 import BeautifulSoup

class PriceScraper:
    def __init__(self):
        self.headers = {"User-Agent": "Defined"}

    def price_scrape(self, url):
        response = requests.get(
            url=url,
            headers=self.headers).text
        soup = BeautifulSoup(response, "lxml")
        return float(soup.find(name="span", class_="a-offscreen").text[1:])


