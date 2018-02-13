from twilio.rest import Client
class SMS:
    def __init__(self,account_sid,auth_token,from_phone,to_phone, msg):
        self.client = Client(account_sid, auth_token)
        message = self.client.messages.create(
            to=to_phone,
            from_=from_phone,
            body=msg)
