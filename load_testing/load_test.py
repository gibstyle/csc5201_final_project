from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)  # wait time between requests, in seconds

    @task
    def index_page(self):
        self.client.get("/")  # Adjust the URL as needed

