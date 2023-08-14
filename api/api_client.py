# api/api_client.py

import requests

BASE_URL = 'https://www.autodl.com/api/v1/dev'


class APIClient:

    def __init__(self, api_token):
        self.api_token = api_token

    def add_auth_header(self, headers):
        headers['Authorization'] = 'token ' + self.api_token
        headers['Content-Type'] = 'application/json'
        return headers

    def post(self, path, json=None, params=None):
        headers = self.add_auth_header({})
        url = BASE_URL + path
        resp = requests.post(url, json=json, params=params, headers=headers)
        return resp.json()

    def get_headers(self):
        headers = {}
        self.add_auth_header(headers)
        return headers

    # def get(self, path, params=None):

    def put(self, path, json=None):
        url = BASE_URL + path
        resp = requests.put(url, json=json, headers=self.get_headers())
        return resp.json()

    def delete(self, path, json=None):
        url = BASE_URL + path
        resp = requests.delete(url, json=json, headers=self.get_headers())
        return resp.json()
