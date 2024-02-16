from cloudant.client import Cloudant
from cloudant.query import Query
from flask import flask, jsonift, request
import atexit

cloudant_username= ''
cloudant_api_key= 'OZXFODn3EjIAN1B7SLt6BnwQi1WhLroIRfWmjI20qiE2'
cloudant_url= 'https://78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix.cloudantnosqldb.appdomain.cloud'