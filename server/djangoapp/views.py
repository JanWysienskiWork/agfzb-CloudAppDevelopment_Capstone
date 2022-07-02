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
    print("thank you "+str(dealer_id))
    if request.method == 'GET':
        url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/dealership"
        dealerships = get_dealers_from_cf(url, **({'id':dealer_id}))
        context['dealer'] = dealerships[dealer_id-1]
        context['cars'] = CarModel.objects.filter(dealerid=dealer_id)
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        url = "https://e767a744.eu-gb.apigw.appdomain.cloud/api/api/review"
        dealer_reviews = get_dealer_reviews_from_cf(url)
        max_id = max([review.id for review in dealer_reviews], default=100)
        new_id = max_id + 1 if max_id >= 100 else max_id + 100
        date = datetime.now()
        date = date.strftime('%Y-%m-%d')
        print(request.POST)
        if 'purchasecheck' in request.POST:
            car=request.POST['car_details']
            car = car.split("-")
            car_make = car[0]
            car_model = car[1]
            car_year = parse(car[2])
            car_year=car_year.year
            print("purchase_date")
            print(request.POST.get('purchase_date'))

            json_payload = {
                'doc': {
                    'id': new_id,
                    'name': request.user.first_name+" "+request.user.last_name,
                    'review': request.POST['review_content'],
                    'purchase': True,
                    'purchase_date': request.POST.get('purchase_date'),
                    'dealership': dealer_id,
                    'car_make': car_make,
                    'car_model': car_model,
                    'car_year': car_year,
                    'review_time': date
                }
            }
        else:
            json_payload = {
                'doc': {
                    'id': new_id,
                    'name': request.user.get_full_name(),
                    'review': request.POST['review_content'],
                    'purchase': False,
                    'dealership': dealer_id,
                    'review_time': date
                   }
            }
        
        json_payload=json.dumps(json_payload)
        print("sending")
        print(json_payload)
        post_request(url, json_payload)
        
        return HttpResponseRedirect(reverse(viewname='djangoapp:dealer_details', args=(str(dealer_id),)))
