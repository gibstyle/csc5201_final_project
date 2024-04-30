import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pickle
import time

database_path = 'review_predictions.db'


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect(database_path)
        self.create_statistics_table()


    def __del__(self):
        self.conn.commit()
        self.conn.close()

    
    def create_statistics_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Statistics" (
          statistic_id INT PRIMARY KEY,
          Endpoint VARCHAR(255),
          Method VARCHAR(255),
          CreatedOn Date DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)


class StatisticsTable:
    TABLENAME = "Statistics"

    def __init__(self):
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row


    def __del__(self):
        self.conn.commit()
        self.conn.close()

    
    def create(self, params):
        query = f'insert into {self.TABLENAME} ' \
                f'(Endpoint, Method, CreatedOn) ' \
                f'values ("{params.get("Endpoint")}","{params.get("Method")}","{params.get("CreatedOn")}")'
        self.conn.execute(query)
    

    def list_statistics(self):
        query = f"SELECT Endpoint, Method, count(*) FROM {self.TABLENAME} GROUP BY Endpoint, Method"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


class ReviewPredictionModel:
    def __init__(self):
        self.models_dir = 'models'
        self.model = None
        self.tfidf = None


    def train(self, data):
        start = time.time()

        # get the data 
        df = pd.DataFrame(data)

        # map ratings to 0 as bad, 1 as ok, and 2 as good, and -1 if invalid
        def map_ratings(rating):
            if rating >= 1.0 and rating <= 2.99:
                return 0
            elif rating >= 3.0 and rating <= 5.0:
                return 1
            else:
                return -1
            
        df['Rating'] = df['Rating'].apply(map_ratings)
        
        # drop rows that are invalid rating
        df = df[df['Rating'] != -1]

        # split into training and testing
        X_train, X_test, y_train, y_test = train_test_split(df['Description'], df['Rating'], test_size=0.2, stratify=df['Rating'])
        
        # use tf-idf to create matrix of words
        self.tfidf = TfidfVectorizer()
        X_train = self.tfidf.fit_transform(X_train)
        X_test = self.tfidf.transform(X_test)

        self.model = RandomForestClassifier()
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)

        training_time = time.time() - start

        # save model and tfidf
        with open(f'{self.models_dir}/model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(f'{self.models_dir}/tfidf.pkl', 'wb') as f:
            pickle.dump(self.tfidf, f)

        return {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Precision': precision_score(y_test, y_pred, average='weighted'),
            'Recall': recall_score(y_test, y_pred, average='weighted'),
            'F1-Score': f1_score(y_test, y_pred, average='weighted'),
            'Training Time': f'{round(training_time, 4)} seconds'
        }


    def predict(self, review):
        if self.model is None:
            return {'Error': 'Model has not been trained.'}
        rating = self.model.predict(self.tfidf.transform([review]))
        if rating == 0:
            ret = 'Bad'
        elif rating == 1:
            ret = 'Good'
        return {'Rating': ret}
    