from twilio import twiml
# from twilio.rest import Client
from flask import Flask, request, redirect, send_file
import requests
from twilio.twiml.messaging_response import MessagingResponse
from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN

import pickle
import json
import numpy as np
import pandas as pd
import re 

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()
    category = ""
    size = ""
    responded = False
    posCat = ['Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy']
    posSize = ['small', 'mid', 'big']
    print(incoming_msg)
    if (incoming_msg.lower() in posCat):
        category = incoming_msg
        msg.body("Would you like to donate to a 'small', 'mid' or 'big' organization?")
    if (incoming_msg in posSize):
        size = incoming_msg.lower()
        print(size)
        msg.body(get_org_recs(category, size))
        responded = True
    if not responded:
        msg.body("Hi there! Which category do you want to donate to:'Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy'?")
    return str(resp)

input_file = 'CLEAN_charity_data.csv'
df = pd.read_csv(input_file, header=0, \
    sep=',',index_col=False, encoding='utf8',lineterminator='\n')

def get_org_recs(category, size):
    # df is initialized in main method.
    df_cat = df.loc[df['category'] == category]
    df_size = df_cat.loc[df['size'] == size]
    df_sorted = df_size.sort_values('score', ascending=False)
    a = df_sorted.iloc[0]['name'] + ", "
    b = df_sorted.iloc[1]['name'] + ", "
    c = df_sorted.iloc[2]['name'] + ""
    recomended_orgs = a + b + c
    return recomended_orgs


def start_ngrok():
    from twilio.rest import Client
    from pyngrok import ngrok

    account = TWILIO_ACCOUNT
    token = TWILIO_TOKEN
    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url)
    client = Client(account, token)
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=url + '/bot')


if __name__ == "__main__":
    # print(get_org_recs("Environment", "small"))
    start_ngrok()
    app.run(debug=True)