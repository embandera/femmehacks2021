from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=("GET", "POST"))
def mms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    msg = resp.message("The Robots are coming! Head for the hills!")

    # Add a picture message
    msg.media("https://farm8.staticflickr.com/7090/6941316406_80b4d6d50e_z_d.jpg")

    return str(resp)


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    url = ngrok.connect(5000).public_url
    print(" * Tunnel URL:", url)
    client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=f"{url}/bot")

if __name__ == "__main__":
    start_ngrok()
    app.run(debug=True)
