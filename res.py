import requests
url = "http://127.0.0.1:5000/weather"
args = {
    "city": "Saint-Petersburg",
    "date_from": "2024-03-25",
    "date_to": "2024-03-26"
}
response = requests.get(url, args)
print(response.json())