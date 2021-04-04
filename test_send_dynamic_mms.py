from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['GET', 'POST'])
def bot():
    inb_msg = request.form['Body'].lower().strip()
    resp = MessagingResponse()

    if inb_msg == "hi":
        msg = resp.message("hi")
        msg.media("https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg")
    else:
        resp.message("else still hi, no image")

    # should this be a string or a MessagingResponse object?
    return "hello"


def start_ngrok():
    from pyngrok import ngrok
    from twilio.rest import Client

    url = ngrok.connect(5000).public_url
    print(f" * Tunnel: {url}")

    account_sid, auth_token = TWILIO_ACCOUNT, TWILIO_TOKEN
    client = Client(account_sid, auth_token)
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=f"{url}/bot")

if __name__ == "__main__":
    start_ngrok()
    app.run(debug=True)





    

