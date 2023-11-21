from twilio.rest import Client

# Twilio config
ACCOUNT_SID = 'AC55463228a82c7bcdf8aca17873ce1312'
AUTH_TOKEN = 'd97c324c1da5b0db2adb5ffb0e62b063'
FROM_NUMBER = '+15209996998'

class Messager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)
        # self.account_sid = os.environ['TWILIO_ACCOUNT_SID']
        # self.auth_token = os.environ['TWILIO_AUTH_TOKEN']
        self.to_number = '+18572723202'

    def send_message(self, msg):
        message = self.client.messages.create(
            body = msg,
            from_= FROM_NUMBER,
            to= self.to_number
        )

if __name__ == '__main__':
    twilio = Messager()
    twilio.send_message('Hello, World!!!!!!')