import requests
from bs4 import BeautifulSoup

class PriceParser:
    def __init__(self, headers, price_selector):
        self.headers = headers
        self.price_selector = price_selector


    def parse_url(self, url):
        page = requests.get(url)
        bs = BeautifulSoup(page.content, "html.parser")
        price = bs.select_one(self.price_selector)
        return price.text.strip()


    def get_price_or_null(self, url):
        try:
            return self.parse_url(url)
        except:
            return None


    def parse_prices(self, urls):
        res = {}
        for url in urls:
            if not url:
                continue
            res[url] = self.get_price_or_null(url)
        return res
