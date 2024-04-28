"""
This is a script used to run locally that will post reviews to the restaurant_review_service.

CSV SOURCES: 
- https://www.kaggle.com/datasets/joebeachcapital/restaurant-reviews
- https://www.kaggle.com/datasets/farukalam/yelp-restaurant-reviews
"""
import pandas as pd
import requests

url = "http://127.0.0.1:8080/review"

# Random
df = pd.read_csv("Restaurant reviews.csv")
df.drop(columns=['Metadata', 'Time', 'Pictures', '7514', 'Reviewer'], inplace=True)
df = df[df['Review'].notna()]
df.rename(columns={'Review': 'Description', 'Restaurant': 'RestaurantName'}, inplace=True)
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
df = df.dropna()

for idx, row in df.iterrows():
    requests.post(url, json={'RestaurantName': row['RestaurantName'],
                             'Description': row['Description'],
                             'Rating': row['Rating'],})


# Yelp
df = pd.read_csv('Yelp Restaurant Reviews.csv')
df['Rating'] = df['Rating'].astype(float)
def extract_restaurant_name(url):
    url_parts = url.split('/')
    restaurant_name = url_parts[-1]
    restaurant_name_cleaned = ' '.join(restaurant_name.split('-'))
    return restaurant_name_cleaned

df['RestaurantName'] = df['Yelp URL'].apply(extract_restaurant_name)
df.drop(columns=['Date', 'Yelp URL'], inplace=True)
df = df[df['Review Text'].notna()]

for idx, row in df.iterrows():
    requests.post(url, json={'RestaurantName': row['RestaurantName'],
                             'Description': row['Review Text'],
                             'Rating': row['Rating'],})
