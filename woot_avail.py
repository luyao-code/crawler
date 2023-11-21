import boto3
import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

# Twilio config
ACCOUNT_SID = 'your_account_sid'
AUTH_TOKEN = 'your_auth_token'
FROM_NUMBER = 'your_twilio_number'
TO_NUMBER = 'your_phone_number'

# Woot product URL
PRODUCTS = {
    'Microsoft Audio Dock': 'https://electronics.woot.com/offers/new-microsoft-audio-speaker-phone-pass-through-charging-dock-2?cjdata=MXxOfDB8WXww&utm_medium=affiliate&utm_campaign=CJ&cjevent=55a6c94b87ad11ee818b04000a82b839&utm_source=dealmoon.com',
}

def check_availability():
    avail = {}
    for name, url in PRODUCTS.items():
        try:
            response = requests.get(url)
            response.raise_for_status()
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            found = soup.find(string="Add to cart")
            if found:
                avail[name] = True
        except requests.RequestException as e:
            pass
    return avail

def send_message(msg):
    client = Client(ACCOUNT_SID, AUTH_TOKEN, msg)
    message = client.messages.create(
        body = msg,
        from_= FROM_NUMBER,
        to= TO_NUMBER
    )
    print(f"Notification sent: {message.sid}")

def main():
    avail = check_product_availability()
    msg = ''
    for name, available in avail.items():
        msg += f"Woot.com: {name} is available now!\nLink: {PRODUCTS[name]}\n\n"
    send_message(msg)

if __name__ == "__main__":
    main()
