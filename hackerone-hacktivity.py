#!/usr/bin/env python3
from json.tool import main
import sys
import requests
import json

my_arr = []


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOTAPI}/sendMessage"
    params = {
        "chat_id": {CHATID}, 
        "text": message
    }
    response = requests.get(url, params=params)
    if response.json()["ok"]:
        print("Mesaj gönderildi.")
    else:
        print("Mesaj gönderilirken bir hata oluştu.")


def hackerone_hackitivity():
    while True:
        headers = {'Content-Type':'application/json'}
        data = '{"operationName":"HacktivityPageQuery","variables":{"querystring":"","where":{"report":{"disclosed_at":{"_is_null":false}}},"orderBy":null,"secureOrderBy":{"latest_disclosable_activity_at":{"_direction":"DESC"}},"count":5},"query":"query HacktivityPageQuery($querystring: String, $orderBy: HacktivityItemOrderInput, $secureOrderBy: FiltersHacktivityItemFilterOrder, $where: FiltersHacktivityItemFilterInput, $count: Int, $cursor: String) {\n  hacktivity_items(first: $count, after: $cursor, query: $querystring, order_by: $orderBy, secure_order_by: $secureOrderBy, where: $where) {\n    ...HacktivityList\n  }\n}\n\nfragment HacktivityList on HacktivityItemConnection {\n    edges {\n    node {\n      ... on HacktivityItemInterface {\n        ...HacktivityItem\n      }\n    }\n  }\n}\n\nfragment HacktivityItem on HacktivityItemUnion {\n  ... on Undisclosed {\n    id\n    ...HacktivityItemUndisclosed\n  }\n  ... on Disclosed {\n    ...HacktivityItemDisclosed\n  }\n  ... on HackerPublished {\n    ...HacktivityItemHackerPublished\n  }\n}\n\nfragment HacktivityItemUndisclosed on Undisclosed {\n  reporter {\n    username\n    ...UserLinkWithMiniProfile\n  }\n  team {\n    handle\n    name\n     url\n    ...TeamLinkWithMiniProfile\n  }\n  latest_disclosable_action\n  latest_disclosable_activity_at\n  requires_view_privilege\n  total_awarded_amount\n  currency\n}\n\nfragment TeamLinkWithMiniProfile on Team {\n  handle\n  name\n }\n\nfragment UserLinkWithMiniProfile on User {\n  username\n}\n\nfragment HacktivityItemDisclosed on Disclosed {\n  reporter {\n    username\n    ...UserLinkWithMiniProfile\n  }\n  team {\n    handle\n    name\n    url\n    ...TeamLinkWithMiniProfile\n  }\n  report {\n    title\n    substate\n    url\n  }\n  latest_disclosable_activity_at\n  total_awarded_amount\n  severity_rating\n  currency\n}\n\nfragment HacktivityItemHackerPublished on HackerPublished {\n  reporter {\n    username\n    ...UserLinkWithMiniProfile\n  }\n  team {\n    handle\n    name\n    medium_profile_picture: profile_picture(size: medium)\n    url\n    ...TeamLinkWithMiniProfile\n  }\n  report {\n    url\n    title\n    substate\n  }\n  latest_disclosable_activity_at\n  severity_rating\n}\n"}'.replace('\n','\\n')
        main_data = requests.post("https://hackerone.com/graphql", data=data, headers=headers)
        main_data = json.loads(main_data.text)
        main_data = main_data['data']['hacktivity_items']['edges']
        for i in range(len(main_data)):
            data=main_data[i]['node']
            reported_to=data['team']['name']
            report_title = data['report']['title']
            report_url = data['report']['url']
            award_amount = data['total_awarded_amount']
            message = f"Yeni bir hackerone raporu yayınlandı! \n\nFirma: {reported_to} Başlık: {report_title} Ödül: {award_amount}$\n{report_url} "
            if report_url in my_arr:
                continue
            else:
                if len(my_arr) == 5:
                    print(reported_to,"|",report_title,"|",report_url,"|",award_amount)
                    send_telegram_message(message)
                    for i in range(1,4):
                        my_arr[i-1] = my_arr[i]
                    my_arr[4] = report_url
                else:
                    my_arr.insert(len(my_arr),report_url)
                    print(reported_to,"|",report_title,"|",report_url,"|",award_amount)
                    send_telegram_message(message)


hackerone_hackitivity()