import requests
from twilio import Twilio
from dynamodb import DynamoDB
from bs4 import BeautifulSoup

# Woot product URL
PRODUCTS = {
    'Microsoft Audio Dock': 'https://electronics.woot.com/offers/new-microsoft-audio-speaker-phone-pass-through-charging-dock-2?cjdata=MXxOfDB8WXww&utm_medium=affiliate&utm_campaign=CJ&cjevent=55a6c94b87ad11ee818b04000a82b839&utm_source=dealmoon.com',
    'MacBook': 'https://computers.woot.com/offers/new-apple-13-3-macbook-air-with-m1-chip-2020z?ref=w_gw_dd_3'
}

def check_availability():
    prod = []
    for name, url in PRODUCTS.items():
        # If the product is already available, skip it.
        if db.get(name)['Item']['avail']:
            continue
        try:
            # Make the request
            response = requests.get(url)
            response.raise_for_status()
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            in_stock = soup.find(string="Add to cart")
            if in_stock:
                db.update(name, 'False')
                prod.append(name)
        except requests.RequestException as e:
            pass
    return prod

if __name__ == "__main__":
    # Initialize DynamoDB and Twilio client.
    db = DynamoDB()
    twilio = Twilio()

    # If the product is not in DynamoDB, add it.
    # The default availability is False.
    for name, url in PRODUCTS.items():
        prod = db.get(name)
        if not prod.get('Item'):
            db.add(name, 'False', url)

    # Get available products.
    prod = check_availability()

    # Build the message.
    msg = ''
    for name in prod:
        msg += f"Woot.com: {name} is available now!\nLink: {PRODUCTS[name]}\n\n"
    twilio.send_message(msg)