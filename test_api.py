import requests
import json

json_body = {"genre": "роман"}


response = requests.put("http://127.0.0.1:5000/api/books/2", json=json_body)
print(response.status_code)

print(requests.get("http://127.0.0.1:5000/api/books").json())

