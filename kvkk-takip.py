import requests
from bs4 import BeautifulSoup
import time
import json
import os

TELEGRAM_BOT_TOKEN = ''
TELEGRAM_CHAT_ID = ''

url = 'https://www.kvkk.gov.tr/veri-ihlali-bildirimi/'

sonicerik_file = 'sonicerik.txt'

def send_telegram_message(message):
    telegram_api_url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    requests.post(telegram_api_url, data=data)

def check_website_for_changes():
    try:
        if os.path.exists(sonicerik_file):
            with open(sonicerik_file, 'r') as file:
                sonicerik = file.read()
        else:
            sonicerik = ''

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            latest_post_title = soup.find('h3', class_='blog-post-title')
            a_tag = soup.find('a', class_='arrow-link all-items')
            siteurl = a_tag['href']

            if latest_post_title and latest_post_title.text.strip() != sonicerik:
                send_telegram_message(f' {latest_post_title.text.strip()} \n https://kvkk.gov.tr{siteurl} ')

                with open(sonicerik_file, 'w') as file:
                    file.write(latest_post_title.text.strip())
        else:
            print(f'Web sitesine erişim hatası: {response.status_code}')

    except Exception as e:
        print(f'Hata: {e}')

if __name__ == '__main__':
    while True:
        check_website_for_changes()

        time.sleep(21600)  # 6 saat