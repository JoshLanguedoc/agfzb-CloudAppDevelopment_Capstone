from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealers_by_state, get_dealer_reviews_from_cf, analyze_review_sentiments
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


#about view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


#contact view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


#login_request view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST": #If request method is POST...
        username = request.POST['username'] #get username from request
        password = request.POST['psw'] #get password from request

        user = authenticate(username=username, password=password) #Check if credentials are valid
        
        if user is not None: #if credentials are valid...
            login(request, user) #login user with login method
            return redirect('djangoapp:about') #redirect user to about page
        else: #if credentials are not valid...
            return redirect('djangoapp:about') #redirect user to login page
    else: #if request method is not POST...
        return redirect('djangoapp:about') #redirect user to login page

#logout_request view to handle sign out request
def logout_request(request):
    logout(request)#logout user with logout method
    return redirect('djangoapp:about')#redirect user back to about page

#registration_request view to handle sign up request
def registration_request(request):
    # Check whether request method is GET or POST and render signup page or attempt to register user respectively
    context = {}
    if request.method == "GET": #if request method is GET...
        return render(request, 'djangoapp/registration.html', context) #render signup page
    elif request.method == "POST": #if request method is POST...
        email = request.POST['email'] #get email from request
        username = request.POST['username'] #get username from request
        firstName = request.POST['first_name'] #get first name from request
        lastName = request.POST['last_name'] #get last name from request
        pswrd = request.POST['psw'] #get password from request

        user_exists = False #Create a boolean to track whether or not user already exists

        try:
            User.objects.get(username=username) #check if user already exists, if not an exception will be thrown
            user_exists = True #with no exception thrown we know a user is already registered with that name
        except: #catch the exception thrown if no user exists
            logger.debug("{} is a new user".format(username)) #log {username} is a new user
        
        if not user_exists: #if user_exists is false...
            #register user:
            user = User.objects.create_user(email= email, username= username, first_name= firstName, last_name= lastName, password= pswrd)
            login(request, user) #log new user in
            return redirect('djangoapp:about')
        else: #is user_exists is true...
            context= {'message': "That username is alread in use, please try another."}
            return render(request, 'djangoapp/registration.html', context) #rerender registration page


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    
    context = {}
    if request.method == "GET":
        url = "https://joshlanguedo-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        try:
            dealerId = request.GET['dealerId']
        except:
            dealerId = False
        try:
            state = request.GET['state']
        except:
            state = False

        if dealerId:
            print("get by ID")
            dealerships = get_dealer_by_id(url, dealerId)

            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

            return HttpResponse(dealer_names)
        
        elif state:
            print("get by State")
            dealerships = get_dealers_by_state(url, state)

            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

            return HttpResponse(dealer_names)

        else:
            print("get all")
            dealerships = get_dealers_from_cf(url)

            dealer_names = ' '.join([dealer.short_name for dealer in dealerships])

            return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealershipurl = "https://joshlanguedo-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        reviewsurl = "https://joshlanguedo-5000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        
        dealership = get_dealer_by_id(dealershipurl, dealer_id)
        reviews = get_dealer_reviews_from_cf(reviewsurl, dealer_id)

        dealername = dealership.short_name
        reviewlist = ''.join([review.review for review in reviews])

        dealerdetails = dealername+reviewlist

        return HttpResponse(dealerdetails)

def testingNLU(request):
    text = "This is great"
    analyze_review_sentiments(text)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

