import requests

url = 'http://localhost:5000/auth'

data = {
    'state': 0,
    'email': 'example@example.com'
}

response = requests.post(url, json=data)
if response.status_code == 200:
    result = response.json()
    token = result.get('token')
    print('Token:', token)
else:
    print('Error:', response.status_code)