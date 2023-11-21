import boto3

class DynamoDB:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def put_item(self, dictionary):
        self.table.put_item(Item=dictionary)

    def get_item(self, key):
        return self.table.get_item(Key=key)
    
if __name__ == '__main__':
    db = DynamoDB('product_avail')
    db.put_item({'product': 'ps', 'avail': False, 'url': 'http://www.woot.com'})
    
