from flask import Flask, request, jsonify
from services import RestaurantReviewService
from models import Schema

app = Flask(__name__)

@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


###################################################################################################
# Reviews
###################################################################################################
@app.route("/review", methods=["GET"])
def list_reviews():
    return jsonify(RestaurantReviewService().list_reviews())


@app.route("/review", methods=["POST"])
def create_review():
    return jsonify(RestaurantReviewService().create_review(request.get_json()))


@app.route("/review/<review_id>", methods=["PUT"])
def update_review(review_id):
    return jsonify(RestaurantReviewService().update_review(review_id, request.get_json()))


@app.route("/review/<review_id>", methods=["GET"])
def get_review(review_id):
    return jsonify(RestaurantReviewService().get_review_by_id(review_id))


@app.route("/review/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    return jsonify(RestaurantReviewService().delete_review(review_id))


###################################################################################################
# Restaurants
###################################################################################################
@app.route("/restaurant", methods=["GET"])
def list_restaurants():
    return jsonify(RestaurantReviewService().list_restaurants())


@app.route("/restaurant/<restaurant_id>", methods=["GET"])
def get_restaurant(restaurant_id):
    return jsonify(RestaurantReviewService().get_reviews_by_restaurant(restaurant_id))


###################################################################################################
# Training data
###################################################################################################
@app.route("/training_data", methods=["GET"])
def get_training_data():
    return jsonify(RestaurantReviewService().get_training_data())


###################################################################################################
# Main
###################################################################################################
if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0', port=8080)
