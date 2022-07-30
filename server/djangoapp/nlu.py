import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

apikey = "vWm5qW_126Mv01yAOrW_gGRwwjTFeleQhJS76zs8OqgQ"
url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/d7024fd9-f76a-459c-a527-4a50a79119f1"

authenticator = IAMAuthenticator(apikey)
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(url)

def get_sentiment(text):
    """Find sentiment for the given text"""
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())).get_result()
    sentiment = response['sentiment']['document']['label']
    return sentiment
