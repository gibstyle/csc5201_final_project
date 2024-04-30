from flask import Flask, request, render_template, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import requests
from models import Schema
from services import ReviewPredictionService
import time


app = Flask(__name__)

# setting up access token as some endpoints can only be accessed by authroized users
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)

HEADERS = {'Content-Type': "application/json"}
users = {'master': 'password000'}

RESTAURANT_REVIEW_SERVICE_URL = "http://127.0.0.1:8080"
RPS = ReviewPredictionService()


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, \
                                                         Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


###################################################################################################
# Home
###################################################################################################
@app.route("/")
def main_page():
    ReviewPredictionService().create_statistic({"Endpoint": "/", "Method": "GET", "CreatedOn": time.time()})   
    return render_template('home.html')


###################################################################################################
# Reviews
###################################################################################################
@app.route("/review", methods=["GET"])
def list_reviews():
    ReviewPredictionService().create_statistic({"Endpoint": "/review", "Method": "GET", "CreatedOn": time.time()})   
    response = requests.get(f'{RESTAURANT_REVIEW_SERVICE_URL}/review', headers=HEADERS)
    return render_template('reviews.html', data=response.json())


###################################################################################################
# Restaurants
###################################################################################################
@app.route("/restaurant", methods=["GET"])
def list_restaurants():  
    ReviewPredictionService().create_statistic({"Endpoint": "/restaurant", "Method": "GET", "CreatedOn": time.time()})   
    response = requests.get(f'{RESTAURANT_REVIEW_SERVICE_URL}/restaurant')
    return render_template('restaurants.html', data=response.json())


###################################################################################################
# Machine Learning Training and Prediction
###################################################################################################
@app.route("/train_model", methods=["GET"])
@jwt_required()
def train_model():
    ReviewPredictionService().create_statistic({"Endpoint": "/train_model", "Method": "GET", "CreatedOn": time.time()})
    response = requests.get(f'{RESTAURANT_REVIEW_SERVICE_URL}/training_data')
    return RPS.train_model(response.json())


@app.route("/predict_review", methods=["GET"])
def predict_reviews():
    ReviewPredictionService().create_statistic({"Endpoint": "/predict_review", "Method": "GET", "CreatedOn": time.time()}) 
    return render_template('predict_review.html')


@app.route("/review_result", methods=["POST"])
def review_result():
    ReviewPredictionService().create_statistic({"Endpoint": "/review_result", "Method": "GET", "CreatedOn": time.time()}) 
    review = request.form['review']
    result = RPS.predict_review(review)
    print(result)
    if 'Error' in result:
        return render_template('home.html')
    else:
        return render_template('predicted_rating.html', data=result)


###################################################################################################
# Login
###################################################################################################
@app.route("/login", methods=["GET"])
def login():
    ReviewPredictionService().create_statistic({"Endpoint": "/login", "Method": "GET", "CreatedOn": time.time()}) 
    return render_template('login.html')


@app.route("/after_login", methods=["POST"])
def after_login():
    ReviewPredictionService().create_statistic({"Endpoint": "/after_login", "Method": "POST", "CreatedOn": time.time()}) 
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        HEADERS["Authorization"] = f'Bearer {access_token}'
        return render_template('login_success.html')
    else:
        return render_template('login_fail.html')


###################################################################################################
# Administrative
###################################################################################################
@app.route("/check_authentication", methods=["GET"])
def check_authentication():
    action = request.args.get('action')
    if action == 'statistics':
        response = requests.get('http://127.0.0.1:5001/statistics', headers=HEADERS)
        return render_template('statistics.html', data=response.json())
    else:
        response = requests.get('http://127.0.0.1:5001/train_model', headers=HEADERS)
        return render_template('training_results.html', data=response.json())


@app.route("/statistics", methods=["GET"])
@jwt_required()
def get_statistics():
    ReviewPredictionService().create_statistic({"Endpoint": "/statistics", "Method": "GET", "CreatedOn": time.time()}) 
    return ReviewPredictionService().get_statistics()


###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    Schema()
    RPS.load_model()
    app.run(debug=True, host='0.0.0.0', port=8080)
