# set GOOGLE_APPLICATION_CREDENTIALS="D:/Coding/Whatever-21592b267981.json"

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    # Instantiates a client
	client = language.LanguageServiceClient()

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


# if __name__ == "__main__":
#	app.run()