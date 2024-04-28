import sqlite3

database_path = 'restaurant_reviews.db'

class Schema:
    def __init__(self):
        self.conn = sqlite3.connect(database_path)
        self.create_review_table()


    def __del__(self):
        self.conn.commit()
        self.conn.close()

    
    def create_review_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS "Review" (
          review_id INTEGER PRIMARY KEY AUTOINCREMENT,
          RestaurantName VARCHAR(255),
          Description TEXT,
          Rating FLOAT,
          CreatedOn Date DEFAULT CURRENT_DATE
        );
        """
        self.conn.execute(query)


class ReviewTable:
    TABLENAME = "Review"

    def __init__(self):
        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row


    def __del__(self):
        self.conn.commit()
        self.conn.close()


    def create(self, params):
        query = f'insert into {self.TABLENAME} ' \
                f'(RestaurantName, Description, Rating) ' \
                f'values ("{params.get("RestaurantName")}","{params.get("Description")}","{params.get("Rating")}")'
        result = self.conn.execute(query)
        return self.get_review_by_id(result.lastrowid)


    def delete(self, review_id):
        query = f"DELETE FROM {self.TABLENAME} WHERE review_id = {review_id}"
        self.conn.execute(query)
        return self.list_restaurants()


    def update(self, review_id, update_dict):
        set_query = ", ".join([f'{column} = "{value}"'
                     for column, value in update_dict.items()])

        query = f"UPDATE {self.TABLENAME} " \
                f"SET {set_query} " \
                f"WHERE review_id = {review_id}"
    
        self.conn.execute(query)
        return self.get_review_by_id(review_id)


    def list_reviews(self, where_clause=""):
        if where_clause == "":
            query = f"SELECT review_id, RestaurantName, Description, Rating, CreatedOn FROM {self.TABLENAME} LIMIT 100"
        else:
            query = f"SELECT review_id, RestaurantName, Description, Rating, CreatedOn FROM {self.TABLENAME} {where_clause} LIMIT 100"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result


    def get_review_by_id(self, review_id):
        where_clause = f"WHERE review_id={review_id}"
        return self.list_reviews(where_clause)


    def get_reviews_by_restaurant(self, restaurant_name):
        where_clause = f"WHERE RestaurantName={restaurant_name}"
        return self.list_reviews(where_clause)
    

    def list_restaurants(self):
        query = f"SELECT DISTINCT RestaurantName FROM {self.TABLENAME}"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result
    

    def get_training_data(self):
        query = f"SELECT Description, Rating FROM {self.TABLENAME}"
        result_set = self.conn.execute(query).fetchall()
        result = [{column: row[i]
                  for i, column in enumerate(result_set[0].keys())}
                  for row in result_set]
        return result
    