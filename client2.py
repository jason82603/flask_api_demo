import requests
import json
import jwt
import time

url = "http://127.0.0.1:5000/users"
valid_token = jwt.encode({'timestamp': int(time.time())}, 'password', algorithm = 'HS256')

print(valid_token)

payload = json.dumps({
})
headers = {
  'auth': valid_token,
  'Content-Type': 'application/json'
}

response = requests.get(url, headers=headers)
# response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
