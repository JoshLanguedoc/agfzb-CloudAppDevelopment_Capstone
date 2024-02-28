from cloudant.client import Cloudant
from cloudant.query import Query
from flask import Flask, jsonify, request, abort
import atexit

cloudant_username= '78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix' 
cloudant_api_key= 'OZXFODn3EjIAN1B7SLt6BnwQi1WhLroIRfWmjI20qiE2'
cloudant_url= 'https://78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())



db = client['reviews']

selector={'dealership':'*'}
reviews = db.metadata()
print("Number of docs: ",reviews['doc_count'])
review_id = reviews['doc_count'] + 1
print("Starting new revies ids at: ",review_id)

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET']) #route wrapper for /api/getreviews GET requests
def get_reviews():
    #Checks request for a valid dealership id then returns requested dealership.
    
    dealership_id = request.args.get('dealerId') #get dealership id from request

    if dealership_id is None: #if dealership id it empty...
        return jsonify({"error": "Missing 'id' parameter in the url"}), 400 #return error with missing id message

    try:
        dealership_id = int(dealership_id) #try to retrieve the dealership with id from the dealerships database
    except ValueError: #if value error is returned...
        return jsonify({"error":"'id' parameter must be an integer"}), 400 #return error with not an integer message
    
    selector = { #create selector dictionary
        'dealership': dealership_id #put the dealership id in the selector dictionary
    }

    result = db.get_query_result(selector) #populate result with query results using selector

    data_list = [] #creat empty data_list

    for doc in result: #iterate through result
        data_list.append(doc) #apped each item in result onto data_list
    
    return jsonify(data_list) #return jsonified data_list

@app.route('/api/post_review', methods=['POST']) #route wrapper for /api/post_review POST requests
def post_review():
    #Checks if request has valid json data. Ensures request contains all required information. 
    #Creates a new document in the reviews database to hold review the new review.
    
    if not request.json: #if request.json is not valid json data...
        abort(400, description='Invalid JSON data') #abort operation and return error with invalid data message

    print(request.json)
    review_data = request.json['review'] #populate review_data to equal request data.
    required_fields = ['time', 'name', 'dealership', 'review', 'purchase', 'purchase_date', 'car_make', 'car_model', 'car_year'] #create required_fields list

    for field in required_fields: #iterate through required_fields
        if field not in review_data: #if field is not in review_data...
            abort(400, description=f'Missing required field: {field}') #abort operation and return error with missing field message

    reviews = db.metadata()
    print("Number of docs: ",reviews['doc_count'])
    review_id = reviews['doc_count'] + 1
    print("Starting new revies ids at: ",review_id)

    review_data.update({'id': review_id})
    db.create_document(review_data) #add document to reviews database using review_data to populate
    review_id = review_id + 1
    return jsonify({"message": "Review posted successfully"}), 201 #return success message

if __name__ == "__main__":
    app.run(debug=True)