# import os
# from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio_credentials_private import TWILIO_ACCOUNT, TWILIO_TOKEN, CELLPHONE

# load_dotenv()
app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    user = request.values.get('From', '')
    resp = MessagingResponse()
    resp.message(f'Hello, {user}, thank you for your message!')
    return str(resp)


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url)
    client = Client(TWILIO_ACCOUNT, TWILIO_TOKEN)
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=url + '/bot')


if __name__ == '__main__':
    # if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
    start_ngrok()
    app.run(debug=True)
