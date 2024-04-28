from models import ReviewTable


class RestaurantReviewService:
    def __init__(self):
        self.review_model = ReviewTable()


    def create_review(self, params):
        """
        Create a review.

        :param params: The review data.
        """
        return self.review_model.create(params)


    def update_review(self, review_id, params):
        """
        Update a review.

        :param review_id: The review to update.
        :param params: The data to update the review with.
        """
        return self.review_model.update(review_id, params)
    

    def delete_review(self, review_id):
        """
        Delete a review.

        :param review_id: The review to delete.
        """
        return self.review_model.delete(review_id)


    def list_reviews(self):
        """
        List all of the reviews in the table.
        """
        return self.review_model.list_reviews()


    def get_review_by_id(self, review_id):
        """
        Get a single review.

        :param review_id: The review to get.
        """
        return self.review_model.get_review_by_id(review_id)
    

    def get_reviews_by_restaurant(self, restaurant_id):
        """
        Get all of the reviews based on a certain restaurant.

        :param restaurant_id: The restaurant to get reviews for.
        """
        return self.review_model.get_reviews_by_restaurant(restaurant_id)
    

    def list_restaurants(self):
        """
        List all of the restaurants in the table.
        """
        return self.review_model.list_restaurants()
    

    def get_training_data(self):
        """
        Get training data for NLP.
        """
        return self.review_model.get_training_data()
