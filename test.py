import requests
PARAMS = {"region": "Rabat-Salé-Kénitra", "commune": "Skhirate", "surface": "222", "type": "villa"}
r = requests.post(url = "http://127.0.0.1:9773", json = PARAMS)
data = r.json()['prix']
print(data)