import json
import requests
from bs4 import BeautifulSoup
from dynamodb import DynamoDB
from ses import SimpleEmailService

# Get the list of products
with open('products.json', 'r') as f:
    PRODUCTS = json.load(f)

def check_availability():
    for prod in PRODUCTS:
        # If the product is already available, skip it.
        if db.get(prod['name'])['Item']['avail'].lower() == 'true':
            continue
        try:
            # Make the request and parse the HTML content
            response = requests.get(prod['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            # 这里是 Woot.com 的检查方式, 其他网站可以更改这里来获得判断
            in_stock = soup.find(string="Add to cart")
            if in_stock:
                ses.send_email_for_purchase(prod['name'], prod['url'])
                db.update(prod['name'], 'True')
        except requests.RequestException as e:
            ses.send_email_for_error(e)

def main(event, context):
    # Initialize the DynamoDB and SimpleEmailService.
    global db, ses
    db = DynamoDB()
    ses = SimpleEmailService()
    # Add new product with False default availability.
    for prod in PRODUCTS:
        if not db.get(prod['name']).get('Item'):
            db.add(prod['name'], 'False', prod['url'])
    # Get available products.
    check_availability()

if __name__ == "__main__":
    main()