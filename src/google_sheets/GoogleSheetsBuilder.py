class GoogleSheetsBuilder:
    def __init__(self, sheets, sheet_id):
        self.sheet_id = sheet_id
        self.sheets = sheets


    def create_new_table(self, name):
        body = {
            'requests': [{
                'addSheet': { 'properties': { 'title': name } }
            }]
        }
        return self.sheets.batchUpdate(spreadsheetId=self.sheet_id, body=body).execute()
    

    def duplicate_table(self, source_id, new_name, insert_idx):
        body = {
            'requests': [{
                'duplicateSheet': {
                    'sourceSheetId': source_id,
                    'insertSheetIndex': insert_idx,
                    'newSheetName': new_name
                }
            }]
        }
        return self.sheets.batchUpdate(spreadsheetId=self.sheet_id, body=body).execute()


    def fill_table(self, name, values):
        range = name + "!A1:Z999"
        body = { 'values': values }
        return self.sheets.values().update(spreadsheetId=self.sheet_id, valueInputOption="RAW", range=range, body=body).execute()


    def get_sheet(self, name):
        try :
            return self.sheet.values().batchGet(spreadsheetId=self.sheet_id, ranges=[name]).execute()
        except Exception as ex:
            print(ex, flush=True)
            return None


    def get_key_idx(values, key):
        for i in range(len(values)):
            for j in range(len(values[i])):
                if values[i][j] == key:
                    return i, j

        raise ValueError(f'Key {key} not found in table') 

