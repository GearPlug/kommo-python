import base64
import requests
import json
from urllib.parse import urlencode

from kommo.exceptions import UnauthorizedError, WrongFormatInputError


class Client(object):
    OAUTH_BASE_URL = "https://www.kommo.com/oauth"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    def __init__(self, client_id=None, client_secret=None, domain=None, redirect_uri=None):
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.REDIRECT_URI = redirect_uri
        self.AUTH_URL = f"https://{domain}/"
        self.TOKEN = None

    def auth_headers(self):
        encoded_credentials = base64.b64encode(f"{self.CLIENT_ID}:{self.CLIENT_SECRET}".encode("utf-8")).decode("utf-8")
        self.headers["Authorization"] = f"Basic {encoded_credentials}"
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"

    def authorization_url(self, state=None):
        params = {
            "client_id": self.CLIENT_ID,
            "state": state,
            "mode": "post_message",
        }

        return self.OAUTH_BASE_URL + "?" + urlencode(params)

    def get_access_token(self, code, domain):
        self.AUTH_URL = f"https://{domain}/"
        body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI
        }
        self.auth_headers()
        return self.post("oauth2/access_token", auth_url=True, data=body)

    def refresh_access_token(self, refresh_token):
        body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "redirect_uri": self.REDIRECT_URI
        }
        self.auth_headers()
        return self.post("oauth2/access_token", auth_url=True, data=body)

    def set_token(self, access_token):
        self.headers.update(Authorization=f"Bearer {access_token}")

    def get_account_info(self):
        return self.get("/api/v4/account")

    def list_companies(self):
        return self.get("/api/v4/companies")

    def get_custom_fields_company(self):
        return self.get('/api/v4/companies/custom_fields')

    def list_contacts(self):
        return self.get("/api/v4/contacts")

    def get_custom_fields_contacts(self):
        return self.get('/api/v4/contacts/custom_fields')

    def list_leads(self):
        return self.get("/api/v4/leads")

    def get_custom_fields_leads(self):
        return self.get('/api/v4/leads/custom_fields')

    def list_tasks(self):
        return self.get("/api/v4/tasks")

    def get_custom_fields_tasks(self):
        return self.get('/api/v4/tasks/custom_fields')

    def create_company(self, name: str = None, custom_fields_values: list = None):
        args = locals()
        body = self.set_form_data(args)
        return self.post("api/v4/companies", data=json.dumps([body]))

    def create_contact(self, first_name: str = None, last_name: str = None, custom_fields_values: list = None):
        args = locals()
        body = self.set_form_data(args)
        return self.post("api/v4/contacts", data=json.dumps([body]))

    def create_lead(self, name: str = None, custom_fields_values: list = None):
        args = locals()
        body = self.set_form_data(args)
        return self.post("api/v4/leads", data=json.dumps([body]))

    def create_task(self, text: str = None, complete_till: int = None):
        args = locals()
        body = self.set_form_data(args)
        return self.post("api/v4/tasks", data=json.dumps([body]))

    def list_webhooks(self):
        return self.get("/api/v4/webhooks")

    def create_webhook(self, event_type: str = None, url: str = None):
        data = {
                "destination": url,
                "settings": [
                    event_type
                ],
                "sort": 10
            }
        return self.post("/api/v4/webhooks", data=json.dumps(data))

    def delete_webhook(self, uuid: str = None):
        return self.delete(f"/api/v4/webhooks/{uuid}")

    def get(self, endpoint, **kwargs):
        response = self.request("GET", endpoint, **kwargs)
        return self.parse(response)

    def post(self, endpoint, **kwargs):
        response = self.request("POST", endpoint, **kwargs)
        return self.parse(response)

    def delete(self, endpoint, **kwargs):
        response = self.request("DELETE", endpoint, **kwargs)
        return self.parse(response)

    def request(self, method, endpoint, auth_url=False, **kwargs):
        return requests.request(
            method, self.AUTH_URL + endpoint, headers=self.headers, **kwargs
        )

    def parse(self, response):
        status_code = response.status_code
        if "Content-Type" in response.headers and "application/json" in response.headers["Content-Type"]:
            try:
                r = response.json()
            except ValueError:
                r = response.text
        else:
            r = response.text
        if status_code == 200:
            return r
        if status_code == 204:
            return None
        if status_code == 400:
            raise WrongFormatInputError(r)
        if status_code == 401:
            raise UnauthorizedError(r)
        if status_code == 500:
            raise Exception
        return r

    def set_form_data(self, args):
        data = {}
        for arg in args:
            if args[arg] is not None and arg != "self":
                data.update({f"{arg}": args[arg]})
        return data
