from google_sheets import GoogleSheetsBuilder, GoogleSheetsParser
from parsers import PriceParser
from googleapiclient.errors import HttpError
import json

class Main:
    def __init__(self, selectors, headers, template_sheet_id, sheets, google_sheet_id):
        self.selectors = selectors
        self.headers = headers
        self.template_sheet_id = template_sheet_id
        self.sheetsParser = GoogleSheetsParser(sheets, google_sheet_id)
        self.sheetsBuilder = GoogleSheetsBuilder(sheets, google_sheet_id)


    def fill_prices_in_urls_map(self, shop: str, shop_urls: list):
        if not shop in self.selectors:
            raise KeyError(f'Selector for shop "{shop}" is not present')

        selector = self.selectors[shop]
        parser = PriceParser(self.headers, selector)
        res = list(shop_urls)

        for entry in res:
            url = entry['url']
            entry['price'] = parser.get_price_or_null(url)

        return res


    def get_prices_map(self, urls_map):
        res = dict(urls_map)
        for shop in res:
            try:
                self.fill_prices_in_urls_map(shop, res[shop])
            except KeyError as e:
                print(e, flush=True)

        return res


    def put_price_in_values(self, values, map_entry):
        i, j = map_entry['index']
        price = map_entry['price']
        if len(values[i]) <= j + 1:
            values[i].append(price)
        else:
            values[i][j + 1] = price


    def get_sheet_values_with_prices(self, sheet_values, price_map):
        values = list(sheet_values)
        for shop_name, shop_entries in price_map.items():
            for entry in shop_entries:
                self.put_price_in_values(values, entry)
        return values


    def save_price_map_to_json(self, price_map, path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(price_map, f, ensure_ascii=False, indent=4)


    def parse_prices_to_google_sheet(self, sheet_name):
        try:
            self.sheetsBuilder.duplicate_table(0, sheet_name, 1)
        except HttpError as e:
            print(e, flush=True)

        urls_map = self.sheetsParser.get_urls_map(sheet_name)
        price_map = self.get_prices_map(urls_map)

        try:
            self.save_price_map_to_json(price_map, f'data/prices-{sheet_name}.json')
        except:
            pass

        values = self.get_sheet_values_with_prices(self.sheetsParser.get_sheet_values(sheet_name), price_map)

        try:
            self.sheetsBuilder.fill_table(sheet_name, values)
        except Exception as e:
            print(e, flush=True)

