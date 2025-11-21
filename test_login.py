import requests

url = "http://localhost:8000/api/auth/login"
data = {
    "username": "admin@example.com",
    "password": "admin"
}

try:
    response = requests.post(url, data=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    print(f"Headers: {response.headers}")
except Exception as e:
    print(f"Error: {e}")
