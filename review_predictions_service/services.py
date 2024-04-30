import pickle
from models import StatisticsTable, ReviewPredictionModel


class ReviewPredictionService:
    def __init__(self):
        self.review_prediction_model = ReviewPredictionModel()
        self.models_dir = 'models'
        self.statistics_model = StatisticsTable()


    def train_model(self, data):
        """
        Train the NLP model based on the current data.
        """
        return self.review_prediction_model.train(data)


    def predict_review(self, review):
        """
        Predict a rating of a given review.
        """

        return self.review_prediction_model.predict(review)

    
    def load_model(self):
        """
        Load the stored model using pickle.
        """
        with open(f'{self.models_dir}/model.pkl', 'rb') as f:
            self.review_prediction_model.model = pickle.load(f)

        with open(f'{self.models_dir}/tfidf.pkl', 'rb') as f:
            self.review_prediction_model.tfidf = pickle.load(f)


    def create_statistic(self, params):
        """
        Record that an endpoint was reached.

        :param params: The statistic data.
        """
        self.statistics_model.create(params)


    def get_statistics(self):
        """
        Get the usage statistics for each endpoint.
        """
        return self.statistics_model.list_statistics()
    