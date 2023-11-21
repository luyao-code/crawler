import boto3

class SimpleEmailService:
    def __init__(self):
        self.ses = boto3.client('ses')
        self.to = 'lu.yao@outlook.com'
        self.subject = 'It\'s available on Woot Now!!'
    
    def send_email(self, product, url):
        self.ses.send_email(
            Destination={
                'ToAddresses': [
                    self.to
                ]
            },
            Message={
                'Subject': {
                    'Data': self.subject,
                    'Charset': 'utf-8'
                },
                'Body': {
                    'Html': {
                        'Data': f'<h1>{product} is available on Woot Now!!</h1><p>Click Me To Purchase!<a href="{url}">{url}</a></p>',
                        'Charset': 'utf-8'
                    }
                }
            }
        )