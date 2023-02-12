import json
import requests
import os
import ioutil
import logging
import logrus
import urllib
import yaml

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

def read_config(file):
    with open(file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            channel = config['Channel']
            chat_id = config['ChatID']
            model = config['Model']
            blaze = config['Blaze']
            return channel, chat_id, model, blaze
        except yaml.YAMLError as e:
            print(e)

channel, chat_id, model, blaze = read_config('config.yml')

def getBlazeData():
    colors = []
    data = requests.get(blaze)
    if data.status_code != 200:
        raise Exception("Error getting data from blaze.com")
    result = TotalPages(0, [])
    result = json.loads(data.text)
    for i, v in enumerate(result["records"]):
        if i == 15:
            break
        colors.append(v["color"])
    colors = list(reversed(colors))
    return colors

def convert_to_numbers(colors):
    color_map = {'white': 0, 'red': 1, 'black': 2}
    numbers = [color_map[color] for color in colors]
    input_data = ",".join(str(num) for num in numbers)
    return {"input": input_data}

def callModel(payload):
    headers = {'content-type': 'application/json'}
    response = requests.post(model, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()["output"]
    else:
        print("Erro ao fazer a requisição")


def send_message_to_telegram_channel(text):
    emoji = ""
    message = ""
    if text == "2":
        emoji = "⚫"
    elif text == "1":
        emoji = "🔴"
    elif text == "0":
        emoji = "⚪"
    elif text == "Win":
        emoji = "Win 🏆"
    elif text == "Loss":
        emoji = "Loss 👎"
    else:
        return

    if emoji == "🏆":
        message = "Win " + emoji
    elif emoji == "👎":
        message = "Loss " + emoji
    else:
        message = "A próxima jogada é " + emoji

    encoded_message = urllib.parse.quote(message)
    url = "https://api.telegram.org/bot" + channel + "/sendMessage?chat_id=" + chat_id + "&text=" + encoded_message

    try:
        file = open("logs/requests.log", "a")
    except:
        logging.error("Failed to open file logs/requests.log")
        return

    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        logging.error("Error sending message to telegram channel: " + str(e))
        file.close()
        return

    body = resp.text
    logging.basicConfig(filename="logs/requests.log", level=logging.INFO)
    logging.info(body)
    file.close()

send_message_to_telegram_channel(callModel(convert_to_numbers(getBlazeData())))
