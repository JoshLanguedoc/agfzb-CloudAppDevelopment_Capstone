from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_by_id, \
                    get_dealers_by_state, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import CarModel, CarMake
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
        returnpage = request.headers['Referer'].replace('https://joshlanguedo-8000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/djangoapp/','')
        returnparts = returnpage.split("/")
        print("returnpage: ",returnpage)
        if returnparts[0] == "":
            returnparts[0] = "index"

        if user is not None: #if credentials are valid...
            login(request, user) #login user with login method
            if len(returnparts) > 1:
                return redirect('djangoapp:'+returnparts[0], returnparts[1]) #redirect user to the page they came from
            else:
                return redirect('djangoapp:'+returnparts[0])
        else: #if credentials are not valid...
            #request.session['error_message'] = 'Incorrect username or password'
            messages.add_message(request, messages.ERROR, 'Incorrect username or password')
            if len(returnparts) > 1:
                return redirect('djangoapp:'+returnparts[0], returnparts[1]) #redirect user to the page they came from
            else:
                return redirect('djangoapp:'+returnparts[0])
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
        url = "https://joshlanguedo-3000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/dealerships/get"
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
            context.update({"dealerships": dealerships})
        
        elif state:
            print("get by State")
            dealerships = get_dealers_by_state(url, state)
            context.update({"dealerships": dealerships})

        else:
            print("get all")
            dealerships = get_dealers_from_cf(url)
            context.update({"dealerships": dealerships})
            
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        dealershipurl = "https://joshlanguedo-3000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/dealerships/get"
        reviewsurl = "https://joshlanguedo-5000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/api/get_reviews"
        
        dealership = get_dealer_by_id(dealershipurl, dealer_id)
        reviews = get_dealer_reviews_from_cf(reviewsurl, dealer_id)

        average_sentiment = "No reviews yet"
        if len(reviews) > 0:
            average_sentiment = 0

            for review in reviews:
                if review.sentiment == 'positive':
                    average_sentiment = average_sentiment + 1
                elif review.sentiment == 'negative':
                    average_sentiment = average_sentiment - 1

            
            average_sentiment = average_sentiment / len(reviews)
            if  -1 <= average_sentiment < -0.25:
                average_sentiment = 'Negative'
            elif -0.25 <= average_sentiment <= 0.25:
                average_sentiment = 'Neutral'
            elif 0.25 < average_sentiment <= 1:
                average_sentiment = 'Positive'
            else:
                average_sentiment = 'something went wrong'

        dealername = dealership.full_name
        reviewlist = ''.join(["{Review: " + review.review+". Sentiment: " + review.sentiment + ".}" for review in reviews])

        context.update({'dealername': dealername, 'dealer_id': dealership.id,'average_sentiment': average_sentiment, 'number_of_reviews': len(reviews), 'reviews': reviews})

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealershipurl = "https://joshlanguedo-3000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/dealerships/get"
    user = request.user

    if user.is_authenticated:

        if request.method == "GET":
            dealership = get_dealer_by_id(dealershipurl, dealer_id)
            dealername = dealership.short_name
            print('Dealer Name is: ', dealername)
            cars = CarModel.objects.filter(dealerid = dealer_id).values()
            for car in cars:
                make_name = CarMake.objects.filter(id=car['make_id']).values_list('name')
                print("Make name is: ", make_name[0][0])
                car.update({'make': make_name[0][0]})
            print(cars)
            context.update({'cars': cars, "dealer_id":dealer_id, 'dealername':dealername})
            return render(request, "djangoapp/add_review.html", context)

        if request.method == "POST":
            print(request.POST)
            url = "https://joshlanguedo-5000.theianext-0-labs-prod-misc-tools-us-east-0.proxy.cognitiveclass.ai/api/post_review"
            time = datetime.utcnow().isoformat()
            name = user.username
            dealership = dealer_id
            review = request.POST['content']

            try: 
                if request.POST['purchasecheck'] == 'true':
                    purchase = True
                    car = CarModel.objects.filter(id = request.POST['car']).values()
                    make_name = CarMake.objects.filter(id=car[0]['make_id']).values_list('name')
                    purchase_date = int(request.POST['purchasedate'][:4])
                    car_model = car[0]['name']
                    car_year = car[0]['year']
                    car_make = make_name[0][0]
                    review = {
                        'name': name,
                        'time': datetime.utcnow().isoformat(),
                        'dealership': dealership,
                        'review': review,
                        'purchase': purchase,
                        'purchase_date': purchase_date,
                        'car_make': car_make,
                        'car_model': car_model,
                        'car_year': car_year
                    }
            except:
                purchase = False
                review = {
                    'name': name,
                    'time': datetime.utcnow().isoformat(),
                    'dealership': dealership,
                    'review': review,
                    'purchase': purchase,
                    'purchase_date': "",
                    'car_make':"",
                    'car_model': "",
                    'car_year': ""
                }
            
            json_payload = {'review': review}
            response = post_request(url, json_payload)
            return redirect('djangoapp:dealer', dealer_id=dealer_id)
    
    else:
        error = {'status_code':401, 'message': "Please log in or Sign up to submit a review."}
        
        return redirect('djangoapp:registration')
            
        
