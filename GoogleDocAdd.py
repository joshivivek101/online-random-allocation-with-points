import logging
import datetime
import urllib.request
import googleapiclient.discovery
from google.oauth2 import service_account
from googleapiclient import errors as GoogleAPIClientErros
import io
import requests
import sys
import json

# create logger with file handler
logger = logging.getLogger('emr-logger')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# constants for the script
service_account_json_file_name = "act.json"
scope = ['https://www.googleapis.com/auth/drive']
NUM_RETRIES = 3
emails_to_exclude = []
with open(service_account_json_file_name) as json_file:
    email = json.load(json_file).get('client_email')
emails_to_exclude.append(email)


class GoogleAPIClient:

    def __init__(self):
        self.drive_google_api_client, self.doc_google_api_client = self.create_google_client()

    # create google client
    @staticmethod
    def create_google_client():

        try:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_json_file_name, scopes=scope)

            drive_service = googleapiclient.discovery.build(
                'drive', 'v3', credentials=credentials)
            doc_service = googleapiclient.discovery.build(
                'docs', 'v1', credentials=credentials)

            return drive_service, doc_service

        except (GoogleAPIClientErros.HttpError, Exception) as e:
            logger.error(e)
            raise Exception('Unable to create google client.')


def get_document(service, id):
    return service.files().get(fileId=id, fields='id,name,mimeType,owners,size,webViewLink,createdTime,modifiedTime,parents,md5Checksum,permissions').execute()


def add_header_if_not_exist(service, id):
    content = service.documents().get(documentId=id).execute(num_retries=NUM_RETRIES)
    cont = content.get('headers')

    if cont is None:
        batch_update_payload = {
            "requests": []
        }

        batch_update_payload['requests'].append({
            'createHeader': {
                'type': 'DEFAULT',
                'sectionBreakLocation': {
                    'index': 0
                }
            }
        })

        response = service.documents().batchUpdate(
            documentId=id,
            body=batch_update_payload
        ).execute(num_retries=NUM_RETRIES)


def insert_text_at_beginning(service, id):
    content = service.documents().get(documentId=id).execute(num_retries=NUM_RETRIES)
    keys = content.get('headers').keys()
    for k in keys:
        segmentId = k
    element = content.get('headers').get(segmentId).get('content')
    end_index = element[0].get('endIndex')

    batch_update_payload = {
        "requests": []
    }

    """ Insert text at beginning """
    batch_update_payload['requests'].append({
        'insertText': {
            'text': '------------------------Unofficial------------------------ \n',
            'location': {
                'segmentId': segmentId,
                'index': 0
            }
        }
    })

    if len(batch_update_payload['requests']) > 0:
        response = google_api_client.doc_google_api_client.documents().batchUpdate(
            documentId=id,
            body=batch_update_payload
        ).execute(num_retries=NUM_RETRIES)


def add_style_to_text(service, id):
    content = service.documents().get(documentId=id).execute(num_retries=NUM_RETRIES)
    cont = content.get('headers')
    keys = content.get('headers').keys()
    # print(cont)
    for k in keys:
        segmentId = k
    element = content.get('headers').get(segmentId).get('content')
    end_index = element[0].get('endIndex')

    batch_update_payload = {
        "requests": []
    }

    """ Add red color at beginning"""
    batch_update_payload['requests'].append({
        'updateTextStyle': {
            "textStyle": {
                "backgroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 1,
                            "green": 0,
                            "blue": 0
                        }
                    }
                },
                "foregroundColor": {
                    "color": {
                        "rgbColor": {
                            "red": 1,
                            "green": 1,
                            "blue": 1
                        }
                    }
                }
            },
            "fields": '*',
            "range": {
                "segmentId": segmentId,
                "startIndex": 0,
                "endIndex": end_index
            }
        }
    })

    """Move red text to middle"""
    batch_update_payload['requests'].append({
        'updateParagraphStyle': {
            "paragraphStyle": {
                "alignment": 'CENTER'
            },
            "fields": 'alignment',
            "range": {
                "segmentId": segmentId,
                "startIndex": 0,
                "endIndex": end_index
            }
        }
    })

    if len(batch_update_payload['requests']) > 0:
        # Bulk update API call to replace images of the document
        response = google_api_client.doc_google_api_client.documents().batchUpdate(
            documentId=id,
            body=batch_update_payload
        ).execute(num_retries=NUM_RETRIES)


def remove_watermark(service, id):
    content = google_api_client.doc_google_api_client.documents().get(
        documentId=id).execute(num_retries=NUM_RETRIES)
    cont = content.get('headers')
    keys = content.get('headers').keys()
    # print(cont)
    for k in keys:
        segmentId = k
    element = content.get('headers').get(segmentId).get('content')
    end_index = element[0].get('endIndex')

    batch_update_payload = {
        "requests": []
    }

    """ Insert text at beginning """
    batch_update_payload['requests'].append({
        'deleteContentRange': {
            "range": {
                "segmentId": segmentId,
                "startIndex": 0,
                "endIndex": end_index
            }
        }
    })

    if len(batch_update_payload['requests']) > 0:
        # Bulk update API call to replace images of the document
        response = google_api_client.doc_google_api_client.documents().batchUpdate(
            documentId=id,
            body=batch_update_payload
        ).execute(num_retries=NUM_RETRIES)


def update_file_permission(service, id, permissions, role):
    to_update = []
    domain_permission = {
        "role": role
    }
    for permission in permissions:
        if permission['emailAddress'] in emails_to_exclude or permission['role'] == 'owner':
            pass
        else:
            to_update.append(permission['id'])
    for perm in to_update:
        service.permissions().update(fileId=id, body=domain_permission,
                                     permissionId=perm).execute()


if __name__ == '__main__':
    id = sys.argv[1]
    cmd = sys.argv[2]
    google_api_client = GoogleAPIClient()
    doc = get_document(google_api_client.drive_google_api_client, id)
    if cmd == 'add':
        add_header_if_not_exist(google_api_client.doc_google_api_client, id)
        insert_text_at_beginning(google_api_client.doc_google_api_client, id)
        add_style_to_text(google_api_client.doc_google_api_client, id)
        update_file_permission(
            google_api_client.drive_google_api_client, id, doc['permissions'], 'reader')
    if cmd == 'rm':
        remove_watermark(google_api_client, id)
        update_file_permission(
            google_api_client.drive_google_api_client, id, doc['permissions'], 'writer')
