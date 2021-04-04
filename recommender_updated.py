from twilio_credentials_private import CELLPHONE, TWILIO_NUMBER, TWILIO_ACCOUNT, TWILIO_TOKEN
# from twilio import twiml
from flask import Flask, request, redirect, send_file
# import requests
from twilio.twiml.messaging_response import MessagingResponse

import json
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

# @app.route('/bot', methods=['POST'])
# def bot():
#     incoming_msg = request.values.get('Body', None)
#     resp = MessagingResponse()
#     msg = resp.message()
#     category = ""
#     size = ""
#     responded = False
#     posCat = ['Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy']
#     posSize = ['small', 'mid', 'big']
#     print(incoming_msg)
#     if (incoming_msg.lower() in posCat):
#         category = incoming_msg
#         msg.body("Would you like to donate to a 'small', 'mid' or 'big' organization?")
#     if (incoming_msg in posSize):
#         size = incoming_msg.lower()
#         print(size)
#         msg.body(get_org_recs(category, size))
#         responded = True
#     if not responded:
#         msg.body("Hi there! Which category do you want to donate to:'Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy'?")
#     return str(resp)


# This reworked version of the bot is an improvement on previous code, but not complete/fully working.
# Doesn't return recommendations - right now it only returns a string I am using to debug.
# Improvement: this version of bot will prompt you to provide input for each of the fields we need (category, size).
# Issue: this version doesn't remember value of prev fields collected. Only remembers vlaue of most recent field.

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', None)
    resp = MessagingResponse()
    # category, size = "", "" --> vars reset to empty each time a reply is triggered. Unhelpful to have here.
    responded = False  # resets to False after each reply is triggered. Added code on line 64/69 to get around this.  
    posCat = [
        'Environment', 
        'Arts, Culture, Humanities', 'Religion','Human Services', 
        'Education', 
        'Animals', 
        'International',
        'Health', 
        'Community Development', 
        'Human and Civil Rights',
        'Research and Public Policy'
        ]
    posSize = [
        'small', 
        'mid', 
        'big'
        ]

    posCat = list(map(lambda x: x.lower(), posCat)) # make everything in posCat lowercase

    if incoming_msg.lower().strip() in posCat:
        responded = True
        self.category = incoming_msg # str.capitalize()? look at df to see format
        resp.message("Would you like to donate to a 'small', 'mid' or 'big' organization?")

    if incoming_msg.lower().strip() in posSize:
        responded = True
        self.size = incoming_msg # str.capitalize()? look at df to see format
        resp.message(f"You have requested {self.size} {self.category} charity recommendation")
        # resp.message(get_org_recs(category, size))

    if not responded:
        resp.message("Hi there! Which category do you want to donate to: 'Environment', 'Arts, Culture, Humanities', 'Religion','Human Services', 'Education', 'Animals', 'International','Health', 'Community Development', 'Human and Civil Rights','Research and Public Policy'?")

    print(f" * output: {reply} {self.category} {self.size}")
    return str(resp)

input_file = 'CLEAN_charity_data.csv'
df = pd.read_csv(input_file, header=0, \
    sep=',',index_col=False, encoding='utf8',lineterminator='\n')

def get_org_recs(category, size):
    # memory = json.loads(request.form.get('Memory'))
    df_cat = df.loc[df['category'] == category]
    df_size = df_cat.loc[df['size'] == size]
    df_sorted = df_size.sort_values('score', ascending=False)
    a = df_sorted.iloc[0]['name'] + ", "
    b = df_sorted.iloc[1]['name'] + ", "
    c = df_sorted.iloc[2]['name'] + ""
    recomended_orgs = a + b + c
    return recomended_orgs

def start_ngrok():
    from pyngrok import ngrok
    from twilio.rest import Client

    #automate ngrok
    url = ngrok.connect(5000).public_url
    print(f" * Tunnel: {url}")
    
   # set incoming numbers and webhook
    account_sid, auth_token = TWILIO_ACCOUNT, TWILIO_TOKEN
    client = Client(account_sid, auth_token)
    client.incoming_phone_numbers.list(
        CELLPHONE)[0].update(
            sms_url=f"{url}/bot")


if __name__ == "__main__":
    # print(get_org_recs("Environment", "small"))

    start_ngrok()
    app.run(debug=True)