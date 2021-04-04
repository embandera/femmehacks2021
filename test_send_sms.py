from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN 
from twilio.rest import Client

account_sid = TWILIO_ACCOUNT
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)

# Post SMS
message = client.messages.create(
    to=CELLPHONE, 
    from_=TWILIO_NUMBER,
    body="If you see this, it is working!"
)
print(f"sid: {message.sid}\nmessage: {message.body}")

## Get SMS (doesnt work with test credentials, must use actual creds)
# get_message = client.messages(message.sid).fetch()
# print(f"sid: {get_message.sid}\nget_message: {get_message.body}")