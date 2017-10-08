# set GOOGLE_APPLICATION_CREDENTIALS=Whatever-21592b267981.json

import tweepy
from sklearn import linear_model
import json
import pandas as pd
import requests
from flask import request, Flask, jsonify

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Consumer keys and access tokens, used for OAuth
consumer_key = 'fc8CilHOkkjKKIVmeP1eYboaL'
consumer_secret = '2ygfVDy8Cw0jaJ2eL5WNekDU4d2joD0YGuDJoyugIAKNAa0AN5'
access_token = '778888850391207936-J7XDawUoLsIDpVQLYDYiiVpsk3Fo7dl'
access_token_secret = 'gdOP2AmZUdV3oIyfpwRQPfGBrTe9nQazRo9kZBGOFXVYe'
 
# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
# Creation of the actual interface, using authentication
api = tweepy.API(auth)

app = Flask(__name__)

def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

@app.route('/data')

def data():
    tickerInJSON = request.args.get('stock');
    ticker = str(tickerInJSON);
    a = helloWorld(ticker);  
    return jsonify({'stock price': a[0],'sentiment':a[1]});
def helloWorld(ticker):
    l = []
    b = tweepy.Cursor(api.search,
                               q=ticker,
                               count=1,
                               result_type="mixed",
                               include_entities=True,
                               lang="en",
                               until="2017-09-29",
                                 ).items()
    for t in b:
        l.append(t)

    for d in ["2017-09-30","2017-10-01","2017-10-02","2017-10-03","2017-10-04","2017-10-05","2017-10-06","2017-10-07"]:
        b = tweepy.Cursor(api.search,
                               q=ticker,
                               count=2,
                               result_type="mixed",
                               include_entities=True,
                               lang="en",
                               until=d,
                               since_id=str(l[-1].id)
                                 ).items()
        for t in b:
            l.append(t)
            dates=[]
    for t in l:
        strng = ""
        for i in [t.created_at.year,t.created_at.month,t.created_at.day]:
            if i < 10:
                strng+="0"
            strng+=str(i)
        dates.append(strng)

    import string
    printable = set(string.printable)

    # Instantiates a client
    client = language.LanguageServiceClient()

    # The text to analyze
    s=[]
    m=[]
    for t in l:
        text = _removeNonAscii(t.text)
        document = types.Document(
            content=text,
            type=enums.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
        sentiment = client.analyze_sentiment(document=document).document_sentiment
        s.append(sentiment.score)
        m.append(sentiment.magnitude)
   
    payload ={'fullUrl' :  "https://www.blackrock.com/tools/hackathon/performance?identifiers="+ticker,'parameters' : {
    'identifiers' :  ticker
    },'url' :  "/tools/hackathon/performance"}

    r = requests.get("https://www.blackrock.com/tools/hackathon/performance?identifiers="+ticker, params=payload)
    a =r.json()
    c = json_dumps(a)
    br = [c['resultMap']['RETURNS'][0]['returnsMap'][str(20170929)]['oneDay']]
    br.append(c['resultMap']['RETURNS'][0]['returnsMap'][str(20170928)]['oneDay'])
    br.append(c['resultMap']['RETURNS'][0]['returnsMap'][str(20170930)]['oneDay'])
    for d in range(20171001,20171006):
        br.append(c['resultMap']['RETURNS'][0]['returnsMap'][str(d)]['oneDay'])

    df = pd.DataFrame(
        {'day': dates[:901],
         'magnitude': m,
         'sentiment': s})
    df2 = df.groupby(['day']).mean()
    x = df2['magnitude'].tolist()
    x1 = df2['sentiment'].tolist()
    import numpy as np
    q = np.array([x[:-1],x1[:-1]])
    z = np.array(br)
    x=x[:-1]
    x1=x1[:-1]
    regr = linear_model.LinearRegression()
    regr.fit(q.transpose(), z)
    nw = np.array([[x[-1]],[x1[-1]]])
    p = regr.predict(nw.transpose())
    x = z+[p]
    return [x,x1]

@app.route('/api/number')
def hello_World():
    return '5'


if __name__ == "__main__":
	app.run()