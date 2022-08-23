from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

# About view
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Contact View
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Login Request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Logout Request
def logout_request(request):
    context = {}
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return render(request, 'djangoapp/index.html', context)

# Registration Request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)

# Get Dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"]=dealerships
        return render(request, 'djangoapp/index.html', context)


# Get Dealer Details
def get_dealer_details(request, dealer_id):
    context = {}
    reviews = get_dealer_reviews_from_cf(dealer_id)
    context["dealer_id"] = dealer_id
    context['review_list'] = reviews
    return render(request, 'djangoapp/dealer_details.html', context)

# Add Review
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    if request.method == 'GET':
        url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context['dealer'] = dealerships[dealer_id-1]
        context['cars'] = CarModel.objects.filter(dealerid=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        json_payload = {}
        dealer_reviews = get_dealer_reviews_from_cf(dealer_id)
        max_id = max([review.id for review in dealer_reviews], default=100)
        new_id = max_id + 1 if max_id >= 100 else max_id + 100
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
        print(request.POST)
        car = request.POST['car']
        car = car.split("-")
        car_make = car[0]
        car_model = car[1]
        car_year = car[2]
        print("purchase_date")
        print(request.POST.get('purchase_date'))
        json_payload = {
            'ID': new_id,
            'NAME': "root",
            'DEALERSHIP': dealer_id,
            'REVIEW': request.POST['review'],
            'PURCHASE': "True",
            'ANOTHER': "ANOTHER",
            'PURCHASE_DATE': request.POST.get('purchase_date'),
            'CAR_MAKE': car_make,
            'CAR_MODEL': car_model,
            'CAR_YEAR': car_year,
        } 
        json_payload=json.dumps(json_payload)
        url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/review"
        post_request(url, json_payload)
        
        return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(str(dealer_id),)))
'''
def add_review(request, dealer_id):
    context = {}
    context["dealer_id"] = dealer_id
    review = dict()
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html', context)

    if request.method == "POST":
            if request.user.is_authenticated:
                review['review'] = {}
                review['review']["time"] = datetime.utcnow().isoformat()
                review['review']["dealership"] = dealer_id
                review['review']["review"] = request.POST["review"]
                review['review']["purchase"] = request.POST["purchase"]
                review['review']['purchase_date'] = request.POST['purchase_date'] or "Nil"
                review['review']["car_model"] = request.POST["car_model"] or "Nil"
                review['review']["car_make"] = request.POST["car_make"] or "Nil"
                review['review']["car_year"] = request.POST["car_year"] or "Nil"

                userr = User.objects.get(username=request.user)
                review['review']['id'] = userr.id
                review['review']["name"] = userr.first_name + " " + userr.last_name

                url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/review"
                
                #json_payload = {}
                #json_payload['review'] = review
                
                post_request(url, review, dealerId=dealer_id)

                return redirect('djangoapp:dealer_details', context) 
                '''