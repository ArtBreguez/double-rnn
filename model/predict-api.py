import json
import requests

url = "http://localhost:5000/predict"

class Records:
    def __init__(self, id, created_at, color, roll):
        self.id = id
        self.created_at = created_at
        self.color = color
        self.roll = roll

class TotalPages:
    def __init__(self, total_pages, records):
        self.total_pages = total_pages
        self.records = records

class Config:
    def __init__(self, channel, chatID, blaze, chatGPT, token, model, maxTokens, temperature):
        self.channel = channel
        self.chatID = chatID
        self.blaze = blaze
        self.chatGPT = chatGPT
        self.token = token
        self.model = model
        self.maxTokens = maxTokens
        self.temperature = temperature

lastHash = bytearray(32)
latestColor = ""

def getBlazeData():
    colors = []
    data = requests.get("https://blaze.com/api/roulette_games/history")
    if data.status_code != 200:
        raise Exception("Error getting data from blaze.com")
    result = TotalPages(0, [])
    result = json.loads(data.text)
    for i, v in enumerate(result["records"]):
        if i == 15:
            break
        colors.append(v["color"])
    colors = list(reversed(colors))
    print(colors)
    return colors

def convert_to_numbers(colors):
    color_map = {'white': 0, 'red': 1, 'black': 2}
    numbers = [color_map[color] for color in colors]
    input_data = ",".join(str(num) for num in numbers)
    return {"input": input_data}

def callModel(payload):
    headers = {'content-type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print(response.json())
    else:
        print("Erro ao fazer a requisição")

colors = getBlazeData()
callModel(convert_to_numbers(colors))
