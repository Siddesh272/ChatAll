import requests
import json

facebook_messenger_access_token = "EAAJb4qObFZA4BOyFiRj7G6XDKBgE2C1UlHlHIYmYM4Pmyi0sL7A7RRDJIUrWkXGe94gbZBX4pCXJQ0ZBwTOhZAFFNbS6H9k33Hw1cSMVWelZBD2NPs5EYZCZAX6DVvGT6eDotOAZCtRUYuzKLSKDh9ZA1lGpngEGvZCiT5lhLLOL11fZBNoLoMRZCDFWnezYV2Lqtw0959re6yTq"
facebook_messenger_page_id = "122449060955941"
instagram_business_account_id = "sid_art272"

facebook_session = requests.Session()
facebook_session.headers.update({"Content-Type": "application/json"})
facebook_session.params = {"access_token": facebook_messenger_access_token}

def send_facebook_messenger_message(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = requests.post(
        f"https://graph.facebook.com/v14.0/{facebook_messenger_page_id}/messages",
        json=data
    )
    if response.status_code != 200:
        print("Failed to send message to Facebook Messenger:", response.text)

def send_instagram_message(user_id, message):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": message}
    }
    response = requests.post(
        f"https://graph.facebook.com/v14.0/me/messages/?business_id={instagram_business_account_id}",
        json=data
    )
    if response.status_code != 200:
        print("Failed to send message to Instagram:", response.text)
