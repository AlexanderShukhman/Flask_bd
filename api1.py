import requests
from datetime import date, timedelta
params = {'gender': 'female', 'nat': 'FR'}
response = requests.get("https://randomuser.me/api/", 
				params=params)
print(response.status_code)
print(response.headers)
print(response.text)
print(response.json()['results'][0]['name'])
