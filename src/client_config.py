# client_config.py
from email.policy import HTTP
import os

class ClientConfig(object):
    PUBLIC_KEY = None  # Replace with your public key later
    APP_NAME = 'Text-Replacer-by-drquochoai'
    COMPANY_NAME = 'drquochoai'
    UPDATE_URLS = ['http://localhost:8000/updates']
    MAX_DOWNLOAD_RETRIES = 3
    HTTP_TIMEOUT = 30