from locust import HttpUser, task, between
from faker import Faker
import random

fake = Faker()


class LoginUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks

    @task
    def login(self):
        url = "/api/auth/login"
        headers = {
            "Content-Type": "application/json"
        }
        # Generate random email
        email = f"{fake.user_name()}{random.randint(1000, 9999)}@example.com"
        payload = {
            "email": "thomasgallagher3399@example.com",
            "password": "password"
        }
        response = self.client.post(url, json=payload, headers=headers)

        # Print the response status code and content
        print(f"Email: {email}")
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
