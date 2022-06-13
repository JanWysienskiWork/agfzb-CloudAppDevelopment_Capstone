import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

# Get Request
def get_request(url,**kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    response = requests.get(url, headers={'Content-Type': 'application/json'}, 
    params=kwargs,  auth=HTTPBasicAuth('apikey', '8d53fb76-69da-4dbe-a708-84af826278e9'))
    json_data = json.loads(response.text)
    return json_data

# Post Request
def post_request(url, json, **kwargs):
    response = requests.post(url, params=kwargs, json=payload)
    return response

# Get dealers from cloud functions
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
        for dealer in dealers:
            dealer_content = dealer["content"]
            dealer_data = CarDealer(address=dealer_content["address"], city=dealer_content["city"], full_name=dealer_content["full_name"],
            id=dealer_content["id"], lat=dealer_content["lat"], long=dealer_content["long"],
            short_name=dealer_content["short_name"],
            st=dealer_content["st"], zip=dealer_content["zip"])
            results.append(dealer_data)
    return results

# Get dealer's reviews from cloud functions
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["rows"]
    review_obj.sentiment = analyze_review_sentiments(review_obj.review)


