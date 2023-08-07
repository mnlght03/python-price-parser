class GoogleSheetsParser:
    def __init__(self, sheets, sheet_id):
        self.sheet_id = sheet_id
        self.sheets = sheets


    def get_sheet(self, name):
        return self.sheets.values().batchGet(spreadsheetId=self.sheet_id, ranges=[name]).execute()


    def get_sheet_values(self, name):
        sheet = self.get_sheet(name)
        return sheet['valueRanges'][0]['values']


    def get_key_idx(values, key):
        for i in range(len(values)):
            for j in range(len(values[i])):
                if values[i][j] == key:
                    return (i, j)

        raise ValueError(f'Key {key} not found in table') 


    def get_shops_map(self, values):
        res = {}
        for i in range(len(values[0])):
            shop = values[0][i]
            if shop != '':
                res[shop] = i
        return res


    def get_url_map_entry(self, shop_idx, values_idx, values):
        return dict(url=values[shop_idx], index=[values_idx, shop_idx])


    def get_urls_map(self, page_name):
        page_range = page_name + "!A1:Z999"
        values = self.get_sheet_values(page_range)
        shops = self.get_shops_map(values)
        res = dict()

        for i in range(2, len(values)):
            val = values[i]
            for shop_name, idx in shops.items():
                if not shop_name in res:
                    res[shop_name] = list()

                try:
                    res[shop_name].append(self.get_url_map_entry(idx, i, val))
                except IndexError:
                    pass
                except Exception as e:
                    print(e, flush=True)
                    continue

        return res

