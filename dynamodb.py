import boto3

class DynamoDB:
    def __init__(self, table_name = 'product_avail'):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def add(self, name, avail, url=None):
        self.table.put_item(Item = {
            'product': name,
            'avail': avail,
            'url': url
        })

    def update(self, name, avail):
        self.table.update_item(
            Key={
                'product': name
            },
            UpdateExpression="set avail = :avail",
            ExpressionAttributeValues={
                ':avail': avail
            }
        )

    def get(self, name):
        return self.table.get_item(Key = {
            'product': name
        })
    
if __name__ == '__main__':
    db = DynamoDB('product_avail')
    db.update('PS5', 'Test')
    # product = db.get({'product': 'PS5'})
    # print(product['Item']['avail'])
