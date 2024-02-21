import requests
import json
from .models import CarDealer
from requests.auth import HTTPBasicAuth

def get_request(url, **kwargs):
    # get_request to make HTTP GET requests to dealerships cloudant database
    
    print("kwargs: " + str(kwargs)) #print arguments
    
    print("Get from {}".format(url)) #print url

    try: #try to get a response from database
        response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except: #if error then print network problem message
        print("Network exception occured")

    status_code = response.status_code #set statue_code to equal the response status code
    print("with status {}",format(status_code)) #print response status code
    json_data = json.loads(response.text) #populate json_data with response as a josn
    return json_data #send json data with response

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
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

    results = []

    json_result = get_request(url, dealerId= dealerId)
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
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



