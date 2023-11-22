import boto3

class SimpleEmailService:
    def __init__(self):
        self.ses = boto3.client('ses')
        self._from = 'lu.yao.us@gmail.com'
        self.to = 'lu.yao@outlook.com'
        self.subject = 'Alert'
    
    def send_email_for_purchase(self, product, url):
        self.ses.send_email(
            Source= self._from,
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
                        'Data': f'<h1>{product} is available on Woot Now !!</h1><p>Click Link Below To Purchase!</p><a href="{url}">{url}</a>',
                        'Charset': 'utf-8'
                    }
                }
            }
        )

    def send_email_for_error(self, error):
        self.ses.send_email(
            Source= self._from,
            Destination={
                'ToAddresses': [
                    self.to
                ]
            },
            Message={
                'Subject': {
                    'Data': 'Crawler Error!',
                    'Charset': 'utf-8'
                },
                'Body': {
                    'Html': {
                        'Data': f'<h1>Crawler just hit an error below !!</h1><p>Error Details:</p><p>{error}</p>',
                        'Charset': 'utf-8'
                    }
                }
            }
        )