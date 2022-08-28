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
import uuid

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
            return redirect('djangoapp:index')
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
    return redirect('djangoapp:index')

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
        new_id = str(uuid.uuid4())
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
        try:
            car = request.POST['car']
        except:
            car = " - - "
        car = car.split("-")
        car_make = car[0]
        car_model = car[1]
        car_year = car[2]
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
