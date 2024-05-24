from locust import HttpUser, task, between
from faker import Faker
import random

fake = Faker()


class RegisterUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks

    @task
    def register(self):
        url = "/api/auth/register"
        headers = {
            "Content-Type": "application/json"
        }
        # Generate random user data
        email = f"{fake.user_name()}{random.randint(1000, 9999)}@example.com"
        payload = {
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "email": email,
            "password": "password"
        }
        response = self.client.post(url, json=payload, headers=headers)

        # Print the response status code and content
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")
        print(f"Mail: {email}")


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
