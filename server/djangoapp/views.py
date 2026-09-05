# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request) # Terminate user session
    data = {"userName":""} # Return empty user
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
# @csrf_exempt
def registration(request):
    # Get user info from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    
    try:
        # Check if username already exists in user registry list
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, log this is a new user
        logger.debug("{} is new user".format(username))

    # Add username to registry list if not already in
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(
            username=username, first_name=first_name,
            last_name=last_name, password=password, email=email)
        # Log user in and redirect to list page
        login(request, user)
        data = {"userName":username, "status":"Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName":username, "error":"Already Registered"}
        return JsonResponse(data)

# Render the index page with list of car models
def get_cars(request):

    # Get count of car models, if zero then populate CarModel table with pre-existing data
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()

    # Parse CarModel data into JSON file, return JSON response
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# # Update the `get_dealerships` view to render the index page with
# a list of dealerships all by default, particular state if state is passed
def get_dealerships(request, state="All"):
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200, "dealers":dealerships})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request,dealer_id):
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review in reviews:
            response = analyze_review_sentiments(review['review'])
            print(response)
            review['sentiment'] = response['sentiment']
        return JsonResponse({"status":200, "reviews":reviews})
    else:
        return JsonResponse({"status":400, "message":"Bad Request"})


# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    if(dealer_id):
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200, "dealer":dealership})
    else:
        return JsonResponse({"status":400, "message":"Bad Request"})

# Create a `add_review` view to submit a review
def add_review(request):
    # Check if user is registered and authentic
    if (request.user.is_anonymous == False):
        # Invoked POST request with review dictionary
        data = json.loads(request.body)
        try:
            # Display response from request and return success message
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401, "message":"Error in posting review"})
    else:
        return JsonResponse({"status":403, "message":"Unauthorized"})
        

    

