#!/bin/bash
echo "Congiruing git variables"
git config --global user.email "jlanguedocgit@gmail.com"
git config --global user.name "Jojo42729"
echo "Setting up Couch Import"
bash ./couchimport-setup.sh
export IAM_API_KEY="OZXFODn3EjIAN1B7SLt6BnwQi1WhLroIRfWmjI20qiE2"
export COUCH_URL="https://78bfea69-47f6-42c2-ab2a-fec36de36077-bluemix.cloudantnosqldb.appdomain.cloud"
echo "Setting up Django environment"
cd server
python3 -m pip install -U -r requirements.txt
server python3 manage.py makemigrations djangoapp
server python3 manage.py migrate
echo "Setting up Node.js Environment"
cd ../functions
npm init -y
npm install -s @cloudant/cloudant
npm install express
bash ./setup.sh