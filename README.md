
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
To obtain and set an access token and set it, follow this instructions:
1. **Get authorization url**
```python
url = client.authorization_url(state=None)
# This call generates the url necessary to display the pop-up window to perform oauth authentication
# param state(code) is required for direct request for oauth, for local test isn't necessary
```
2. **Get access token**
```python
access_token = client.get_access_token(code, domain)
# This call generates the oauth validation and get the access token and refresh token.
# Must send the code and domain generated from get authorization url. 
```
3. **Refresh access token**
```python
refresh_token = client.refresh_access_token(refresh_token)
# "refresh_token" is the token refresh in response after login with oauth with the above url.
```

4. **Set token**
```python
client.set_token(access_token)
# It is necessary to be able to use the library's actions.
```
##Actions for get data
- **Get account info**
```python
client.get_account_info()
# Returns a json with the account information where the application was configured.
```

- **Get list of companies**
```python
client.list_companies()
# Returns a json with the list of companies.
```

- **Get custom fields for company**
```python
client.get_custom_fields_company()
# Returns a json with the list of custom fields for company.
```

- **Get list of contacts**
```python
client.list_contacts()
# Returns a json with the list of contacts.
```

- **Get custom fields for contact**
```python
client.get_custom_fields_contacts()
# Returns a json with the list of custom fields for contact.
```

- **Get list of leads**
```python
client.list_leads()
# Returns a json with the list of leads.
```

- **Get custom fields for lead**
```python
client.get_custom_fields_leads()
# Returns a json with the list of custom fields for lead.
```

- **Get list of tasks**
```python
client.list_tasks()
# Returns a json with the list of tasks.
```

- **Get custom fields for task**
```python
client.get_custom_fields_tasks()
# Returns a json with the list of custom fields for tast.
```

##Actions for send data

- **Create company**
```python
client.create_company(name: str = None, company_name: str = None, 
                      phone: str = None, email: str = None,
                      custom_fields: list = None)
# Allows you to create a company in the configured application.
```

- **Create contact**
```python
client.create_contact(self, name: str = None, first_name: str = None, 
                      last_name: str = None,
                      custom_fields: list = None)
# Allows you to create a contact in the configured application.
```

- **Create lead**
```python
client.create_lead(self, name: str = None, first_name: str = None, 
                   last_name: str = None,
                   custom_fields: list = None)
# Allows you to create a lead in the configured application.
```

- **Create lead**
```python
client.create_task(self, name: str = None, first_name: str = None, 
                   last_name: str = None,
                   custom_fields: list = None)
# Allows you to create a task in the configured application.
```

##Actions for webhook

- **List webhooks**
```python
client.list_webhooks()
# Allows list webhooks in the configured application.
```

- **Create webhook**
```python
client.create_webhook(event_type: str = None, url: str = None)
# Allows create a webhook in the configured application.
```

- **Delete webhook**
```python
client.delete_webhook(uuid: str = None)
# Allows delete a webhook in the configured application.
```