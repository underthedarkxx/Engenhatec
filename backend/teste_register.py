import os

import requests

url = "http://127.0.0.1:5000/api/auth/register"

payload = {
    "username": "RobertoD",
    "password": os.environ["TEST_USER_PASSWORD"],
    "email": "roberto@email.com",
    "is_subscribed": True,
}

response = requests.post(url, json=payload)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except Exception:
    print("Resposta não é JSON válida:", response.text)
