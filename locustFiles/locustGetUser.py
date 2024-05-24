from locust import HttpUser, task, between
import json


class GetUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between tasks

    # Predefined OAuth2 token
    oauth2_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY2NTBlNWZmYmI2ODM4MzA0MjYyZTZhNyIsImVtYWlsIjoib2t0YXlAZXhhbXBsZS5jb20iLCJpYXQiOjE3MTY1Nzc3OTcsImV4cCI6MTcxNjY2NDE5N30.Mzo2ewsRwXTYldMH_01UvGzdUDfzasU79QnnexlUnNk"

    @task
    def get_user(self):
        url = "/api/user"
        headers = {
            "Authorization": f"Bearer {self.oauth2_token}",
            "Content-Type": "application/json",
        }
        data = {
            "id": "6650e2d3741aad918b910938"
        }
        response = self.client.get(
            url, headers=headers, data=json.dumps(data))

        # Print the request headers for debugging
        print(f"Request Headers: {headers}")

        # Print the request body for debugging
        print(f"Request Body: {json.dumps(data)}")

        # Print the response status code and content
        print(f"Status Code: {response.status_code}")
        print(f"Response Content: {response.text}")


if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")
