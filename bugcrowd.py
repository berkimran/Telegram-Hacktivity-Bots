import requests
import time
import regex as re
import json

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOTAPI}/sendMessage"
    params = {"chat_id": {CHATAPI}, "text": message}
    response = requests.get(url, params=params)
    if response.json()["ok"]:
        print("Mesaj gönderildi.")
    else:
        print("Mesaj gönderilirken bir hata oluştu.")

def check_report_change():
    prev_id = ""

    while True:
        url = "https://bugcrowd.com/crowdstream.json?page=1&filter_by=disclosures"
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            current_bug = data["results"][0]
        if current_bug['id'] != prev_id:
            message = f"{current_bug['title']}\nProgram: {current_bug['program_name']}\nhttps://bugcrowd.com{current_bug['disclosure_report_url']}"
            send_telegram_message(message)

        prev_id = current_bug['id']
        time.sleep(60 * 120)

check_report_change()