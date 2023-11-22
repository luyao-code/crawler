import requests
from bs4 import BeautifulSoup
from dynamodb import DynamoDB
from ses import SimpleEmailService

# Woot product URL
PRODUCTS = {
    'AudioDock': 'https://electronics.woot.com/offers/new-microsoft-audio-speaker-phone-pass-through-charging-dock-2',
}

def check_availability():
    for name, url in PRODUCTS.items():
        # If the product is already available, skip it.
        if db.get(name)['Item']['avail'].lower() == 'true':
            continue
        try:
            # Make the request and parse the HTML content
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            # 这里是 Woot.com 的检查方式, 其他网站可以更改这里来获得判断
            in_stock = soup.find(string="Add to cart")
            if in_stock:
                ses.send_email_for_purchase(name, url)
                db.update(name, 'True')
        except requests.RequestException as e:
            ses.send_email_for_error(e)

def main(event, context):
    # Initialize the DynamoDB and SimpleEmailService.
    global db, ses
    db = DynamoDB()
    ses = SimpleEmailService()
    # Add new product with False default availability.
    for name, url in PRODUCTS.items():
        prod = db.get(name)
        if not prod.get('Item'):
            db.add(name, 'False', url)
    # Get available products.
    check_availability()

if __name__ == "__main__":
    main()