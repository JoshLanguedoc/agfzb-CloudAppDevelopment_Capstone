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

@app.route('/api/get_reviews', methods=['GET'])
def get_reviews():
    dealership_id = request.args.get('id')

    if dealership_id is None:
        return jsonify({"error": "Missing 'id' parameter in the url"}), 400

    try:
        dealership_id = int(dealership_id)
    except ValueError:
        return jsonify({"error":"'id' parameter must be an integer"}), 400
    
    selector = {
        'dealership': dealership_id
    }

    data_list = []

    for doc in result:
        data_list.append(doc)
    
    return jsonify(data_list)

@app.route('/api/post_review', method=['POST'])
def post_review():
    if not request.json:
        abort(400, description='Invalid JSON data')

    review_data = request.json

    required_fields = ['id', 'name', 'dealership', #Keep going from here this line is not finished]