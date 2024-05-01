from flask import Flask, request, render_template, session, redirect, url_for
from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import requests
from models import Schema
from services import ReviewPredictionService
import time
import logging


logging.basicConfig(filename='logs/all_logs.log', level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s', force=True)

app = Flask(__name__)

# setting up access token as some endpoints can only be accessed by authroized users
# Set secret key
app.secret_key = 'super-secret-key'

HEADERS = {'Content-Type': "application/json"}

RESTAURANT_REVIEW_SERVICE_URL = "http://restaurant_review_service:8080" 
# RESTAURANT_REVIEW_SERVICE_URL = "http://127.0.0.1:8080"

REVIEW_PREDICTION_SERVICE_URL = "http://review_predictions_service:8081"  
# REVIEW_PREDICTION_SERVICE_URL = "http://127.0.0.1:8081"
RPS = ReviewPredictionService()


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, \
                                                         Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('is_admin'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))  # Redirect to login page if not admin
    return wrapper


###################################################################################################
# Home
###################################################################################################
@app.route("/")
def main_page():
    session['is_admin'] = False
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
@admin_required
def train_model():
    ReviewPredictionService().create_statistic({"Endpoint": "/train_model", "Method": "GET", "CreatedOn": time.time()})
    response = requests.get(f'{RESTAURANT_REVIEW_SERVICE_URL}/training_data')
    response = RPS.train_model(response.json())
    return render_template('training_results.html', data=response)



@app.route("/predict_review", methods=["GET"])
def predict_reviews():
    ReviewPredictionService().create_statistic({"Endpoint": "/predict_review", "Method": "GET", "CreatedOn": time.time()}) 
    return render_template('predict_review.html')


@app.route("/review_result", methods=["POST"])
def review_result():
    ReviewPredictionService().create_statistic({"Endpoint": "/review_result", "Method": "GET", "CreatedOn": time.time()}) 
    review = request.form['review']
    result = RPS.predict_review(review)
    logging.info(f'Review: review={review}, result={result}')
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


@app.route("/login_submitted", methods=["POST"])
def after_login():
    ReviewPredictionService().create_statistic({"Endpoint": "/after_login", "Method": "POST", "CreatedOn": time.time()}) 
    username = request.form['username']
    password = request.form['password']
    logging.info(f'Login: username={username}, password={password}')
    
    result = ReviewPredictionService().admin_model.check_admin(username, password)
    if len(result) > 0:
        session['is_admin'] = True
        return render_template('login_success.html')
    else:
        session['is_admin'] = False
        return render_template('login_fail.html')


###################################################################################################
# Administrative
###################################################################################################
@app.route("/statistics", methods=["GET"])
@admin_required
def get_statistics():
    ReviewPredictionService().create_statistic({"Endpoint": "/statistics", "Method": "GET", "CreatedOn": time.time()}) 
    response = ReviewPredictionService().get_statistics()
    return render_template('statistics.html', data=response)



###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    Schema()
    RPS.load_model()
    app.run(debug=True, host='0.0.0.0', port=8081)
