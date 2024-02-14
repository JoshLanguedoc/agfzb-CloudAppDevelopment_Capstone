from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
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
            return render(request, 'djangoapp/user_login.html', context) #redirect user to login page
    else: #if request method is not POST...
        return render(request, 'djangoapp/user_login.html', context) #redirect user to login page

#logout_request view to handle sign out request
def logout_request(request):
    logout(request)#logout user with logout method
    return redirect('djangoapp:about')#redirect user back to about page

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

