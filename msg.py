from twilio.rest import Client

# Twilio config
FROM_NUMBER = '+1234567890'

class Messager:
    def __init__(self):
        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        to_number = os.environ['TWILIO_TO_NUMBER']
        self.client = Client(account_sid, auth_token)
        self.to_number = to_number

    def send_message(self, msg):
        message = self.client.messages.create(
            body = msg,
            from_= FROM_NUMBER,
            to= self.to_number
        )

if __name__ == '__main__':
    twilio = Messager()
    twilio.send_message('Hello, World!!!!!!')