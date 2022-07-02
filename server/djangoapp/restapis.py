import os
import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Get Request
def get_request(url, **kwargs):
    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Post Request
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Get Dealers - cf
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers

        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)

    return results

# Get Dealers' Review - cf
def get_dealer_reviews_from_cf(dealer_id):
    results=[]
    url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/review?dealership=" + str(dealer_id)
    # call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        reviews = json_result["result"]["docs"]
        for rev in reviews:
            review_obj = DealerReview(id=rev["id"], name=rev["name"], dealership=rev["dealership"],
                               review=rev["review"], purchase=rev["purchase"], purchase_date=rev["purchase_date"], 
                               car_make=rev["car_make"], car_model=rev["car_model"], car_year=rev["car_year"])
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)

    return results

# NLU
def analyze_review_sentiments(text):
    kwargs = {
        'text': text,
        'api_key': "diwqh3I4AHXGO2-ifz68x4pNLjgLNmEekt-dyQPItpgs"
    }
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/6be0d2ef-5df8-4af1-b0e2-006d09e49dee"
    result = get_request(url + '/v1/analyze', **kwargs)
    return result['sentiment']['document']['label']
