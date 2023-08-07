import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.errors import HttpError


def get_sacc_service(path_to_json):
    scopes = ['https://www.googleapis.com/auth/spreadsheets']
    service = ServiceAccountCredentials.from_json_keyfile_name(path_to_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=service)


from .GoogleSheetsBuilder import GoogleSheetsBuilder
from .GoogleSheetsParser import GoogleSheetsParser
