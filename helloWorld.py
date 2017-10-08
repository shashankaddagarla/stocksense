# set GOOGLE_APPLICATION_CREDENTIALS="D:/Coding/Whatever-21592b267981.json"
API_KEY='AIzaSyCszc-XwrISKJnkmQUnS05KGFfcBhi9Zzw'

import logging
from logging.handlers import RotatingFileHandler
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # Instantiates a client
	client = language.LanguageServiceClient(key=API_KEY)

	# The text to analyze
	text = u'Hello, world!'
	document = types.Document(
	    content=text,
	    type=enums.Document.Type.PLAIN_TEXT)

	# Detects the sentiment of the text
	sentiment = client.analyze_sentiment(document=document).document_sentiment

	print('Text: {}'.format(text))
	return('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))


@app.route('/api/number')
def helloWorld():
    return '5'


if __name__ == "__main__":
	logHandler = RotatingFileHandler('info.log', maxBytes=1000, backupCount=1)
	logHandler.setLevel(logging.ERROR)
	app.logger.setLevel(logging.ERROR)
	app.logger.addHandler(logHandler)
	app.run()