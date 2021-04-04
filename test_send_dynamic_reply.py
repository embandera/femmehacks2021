from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=('GET', 'POST'))
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get("Body", None)
    print(type(body))
    print(body)
    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body == 'hello ':
        resp.message("Hi!")
    elif body == 'bye':
        resp.message("Goodbye")
    else:
        resp.message("hvkgk")

    return str(resp)


def start_ngrok():
    from pyngrok import ngrok
    from twilio.rest import Client

    url = ngrok.connect(5000).public_url
    print(" * Tunnel: ", url)

    account_sid, auth_token = TWILIO_ACCOUNT, TWILIO_TOKEN
    client = Client(account_sid, auth_token)

    # set incoming numbers and webhook
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=f"{url}/bot")


if __name__ == "__main__":
    start_ngrok()
    app.run(debug=True)