import requests

r = requests.put('http://0.0.0.0:5000/' ,json = {
    "type": "lamp",
    "agent_id": "b07882d6-5c28-597b-89f9-d250f74b0bad",
    "device_id": "1:5",
    "settings": {
        "on": True
    }},headers={'content-type':'application/json'})
