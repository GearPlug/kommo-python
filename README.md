
# kommo-python
![](https://img.shields.io/badge/version-0.1.4-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)  

*kommo-python* is an API wrapper for Kommo CRM, written in Python.  
This library uses Oauth2 for authentication.
## Installing
```
pip install kommo-python
```
### Usage
```python
from kommo.client import Client
client = Client(client_id, client_secret, code, domain, redirect_uri)
```
To obtain and set an access token, follow this instructions:
1. **Get access token**
```python
body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": self.CODE,
            "redirect_uri": self.REDIRECT_URI
        }
access_token = client.get_access_token(body)
# This call generates the oauth validation and get the access token and refresh token
```
2. **Refresh access token**
```python
refresh_token = client.refresh_access_token(refresh_token)
# "refresh_token" is the token refresh in response after login with oauth with the above url.
```
