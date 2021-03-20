import random
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

account_sid = "AC5860a17c2df9813ef653c3ff4e808d1a"
auth_token = "08e2e9abd83c20e5042394d28f1715bb"
client = Client(account_sid, auth_token)


class TwilioSms:
    def __init__(self, to, body):
        self.to = to
        self.body = body

    def send(self):
        try:
            message = client.messages \
                .create(
                body=self.body,
                from_='+15034655860',
                to=f'+2{self.to}'
            )
            return message
        except TwilioRestException as e:
            print(e)


def otp_generator():
    otp = random.randint(999, 9999)
    return otp
