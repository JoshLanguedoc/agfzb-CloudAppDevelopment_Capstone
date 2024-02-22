import requests
import json
from .models import CarDealer, DealerReviews
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    # get_request to make HTTP GET requests to dealerships cloudant database
    
    print("kwargs: " + str(kwargs)) #print arguments
    
    print("Get from {}".format(url)) #print url

    try: #try to get a response from database
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except: #if error then print network problem message
        print("Network exception occured")

    status_code = response.status_code #set statue_code to equal the response status code
    json_data = json.loads(response.text) #populate json_data with response as a josn
    return json_data #send json data with response

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def get_dealers_from_cf(url, **kwargs):
    results = []

    json_result = get_request(url)
    if json_result:
        dealers = json_result

        for dealer in dealers:
            dealer_doc = dealer
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId):

    json_result = get_request(url, dealerId= dealerId)
    print(json_result)
    if json_result:
        dealer_doc = json_result[0]
        
        dealer = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])

    return dealer

def get_dealers_by_state(url, state):
    results = []

    json_result = get_request(url, state=state)
    if json_result:
        dealers = json_result

        for dealer in dealers:
            dealer_doc = dealer
            #print("Dealer", dealer_doc)
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []

    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result

        for review in reviews:
            review_doc = review
            sentiment = analyze_review_sentiments(review_doc['review'])
            if sentiment['status_code'] == 200:
                sentiment_label = sentiment['data']['sentiment']['document']['label']                

            review_obj = DealerReviews(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"], 
                                    review=review_doc["review"], purchase_date=review_doc["purchase_date"], 
                                    car_make=review_doc["car_make"], car_model=review_doc["car_model"], car_year=review_doc["car_year"],
                                    sentiment = sentiment_label, id=review_doc["id"])
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    authenticator = IAMAuthenticator('RNFMuikErrlqY-BKK_RNEvClcPNipKg_rsJ0lWb3ovB8')
    nlu = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    nlu.set_service_url('https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/ef0db16c-6adb-4d00-b088-a8f0575fa0a3')

    print("Analyzing phrase: ",text)
    try:
        analysis = nlu.analyze(
            text = text, 
            features = Features(sentiment=SentimentOptions())
            )
        response = {'data': analysis.get_result(), 'status_code': analysis.get_status_code()}
        
    except ApiException as error:
        print(error.message)
        if error.message == 'not enough text for language id':
            try:
                print('review to short to identify language. Trying with English as specified language.')
                analysis = nlu.analyze(
                    text = text, 
                    features = Features(sentiment=SentimentOptions()),
                    language = 'en'
                    )
                print('English worked')
                response = {'data': analysis.get_result(), 'status_code': analysis.get_status_code()}
            except:
                response = {'data': error.message, 'status_code': error.code}
        else:
            response = {'data': error.message, 'status_code': error.code}

    print(response['data'])
    print(response['status_code'])

    return (response)