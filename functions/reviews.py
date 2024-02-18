from cloudant.client import Cloudant
from cloudant.query import Query
from flask import flask, jsonift, request
import atexit

cloudant_username= 'jlanguedocgit@gmail.com' 
cloudant_api_key= 'OZXFODn3EjIAN1B7SLt6BnwQi1WhLroIRfWmjI20qiE2'
cloudant_url= 'https://78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix.cloudantnosqldb.appdomain.cloud'
client = Cloudant.iam(cloudant_username, cloudant_api_key, connect=True, url=cloudant_url)

session = client.session()
print('Databases:', client.all_dbs())

db = client['review']

app = Flask(__name__)

@app.route('/api/get_reviews', methods=['GET']) #route wrapper for /api/getreviews GET requests
def get_reviews():
    #Checks request for a valid dealership id then returns requested dealership.
    
    dealership_id = request.args.get('id') #get dealership id from request

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

@app.route('/api/post_review', method=['POST']) #route wrapper for /api/post_review POST requests
def post_review():
    #Checks if request has valid json data. Ensures request contains all required information. 
    #Creates a new document in the reviews database to hold review the new review.
    
    if not request.json: #if request.json is not valid json data...
        abort(400, description='Invalid JSON data') #abort operations adn return error with invalid data message

    review_data = request.json #populate review_data to equal request data.

    required_fields = ['id', 'name', 'dealership', 'review', 'purchase_date', 'car_model', 'car_year']
    for field in required_fields:
        if field not in review_data:
            abort(400, description=f'Missing required field: {field}')

    db.create_document(review_data)
    
    return jsonify({"message": "Review posted successfully"}), 201

if __name__ == "__main__":
    app.run(debug=True)