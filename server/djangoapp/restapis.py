import os
import requests
import json
from .nlu import get_sentiment
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
        headers = {  'Content-Type': 'application/json'}
        response= requests.request("POST", url, headers=headers, data=json_payload)

        status_code = response.status_code
        if status_code == 200:
            json_data = json.loads(response.text)
            return json_data
        else:
            print('Response Status Code = ', status_code)
            return None
    except Exception as e:
        print('Error occurred', e)
        return None

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
    url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/review?dealerId=" + str(dealer_id)
    # call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        reviews = json_result["result"]
        for rev in reviews:
            if (rev["purchase"] != False):
                review_obj = DealerReview(id="", name=rev["name"], dealership=rev["dealership"],
                               review=rev["review"], purchase=rev["purchase"], purchase_date=rev["purchase_date"], 
                               car_make=rev["car_make"], car_model=rev["car_model"], car_year=rev["car_year"])
            else:
                review_obj = DealerReview(id="", name=rev["name"], dealership=rev["dealership"],
                               review=rev["review"], purchase=rev["purchase"], purchase_date="", 
                               car_make="", car_model="", car_year="")
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

# NLU
def analyze_review_sentiments(text):
    return get_sentiment(text)
